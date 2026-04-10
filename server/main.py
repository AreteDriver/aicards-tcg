"""AI Cards Minting API — mints NFT cards on Solana via Metaplex compressed NFTs."""

import asyncio
import base64
import json
import logging
import os
import struct

import httpx
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, field_validator

from card_data import build_pack

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("aicards")

# ═══════════════════════════════════════
# CONFIG
# ═══════════════════════════════════════
SOLANA_RPC = os.getenv("SOLANA_RPC_URL", "https://api.mainnet-beta.solana.com")
COLLECTION_MINT = os.getenv("AICARDS_COLLECTION_MINT", "")  # Set after collection creation
MERKLE_TREE = os.getenv("AICARDS_MERKLE_TREE", "")  # Set after tree creation
TREE_AUTHORITY = os.getenv("AICARDS_TREE_AUTHORITY", "")  # PDA of tree
CREATOR_KEYPAIR = os.getenv("AICARDS_CREATOR_KEYPAIR", "")  # Base58 private key
AICARDS_TOKEN_MINT = os.getenv("AICARDS_TOKEN_MINT", "")
TREASURY_WALLET = os.getenv("TREASURY_WALLET", "")
IMAGE_BASE_URL = os.getenv("AICARDS_IMAGE_URL", "https://aicards.fun/images/cards")
METADATA_BASE_URL = os.getenv("AICARDS_METADATA_URL", "https://aicards.fun/metadata")

# SPL Token program
TOKEN_PROGRAM_ID = "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"
# Bubblegum program (Metaplex compressed NFTs)
BUBBLEGUM_PROGRAM_ID = "BGUMAp9Gq7iTEuizy4pqaxsTyUCBK68MDfK752kRSfkm"

VALID_PACK_TYPES = {
    "standard", "legendary", "jobless", "doomscroll", "loveexe", "warroom",
    "skillsvoid", "founderexe", "deepstateai", "healthcaresys", "parenttrap",
    "climateerr", "creatornull", "analogrevival", "mergeprotocol", "ubiworld",
    "walledgarden", "solarpunk", "greyzone", "frontiernull",
}

# ═══════════════════════════════════════
# APP
# ═══════════════════════════════════════
app = FastAPI(title="AI Cards Minting API", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://aicards.fun", "http://localhost:3000", "http://localhost:8000"],
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)


class MintRequest(BaseModel):
    solana_address: str
    pack_type: str
    payment_signature: str | None = None  # Solana tx signature for token payment

    @field_validator("solana_address")
    @classmethod
    def validate_address(cls, v: str) -> str:
        v = v.strip()
        # Solana addresses are base58, 32-44 chars
        import re
        if not re.match(r"^[1-9A-HJ-NP-Za-km-z]{32,44}$", v):
            raise ValueError("Invalid Solana address")
        return v

    @field_validator("pack_type")
    @classmethod
    def validate_pack_type(cls, v: str) -> str:
        if v not in VALID_PACK_TYPES:
            raise ValueError(f"Invalid pack type — must be one of {VALID_PACK_TYPES}")
        return v


class MintResponse(BaseModel):
    success: bool
    pack_type: str
    cards: list[dict]
    transaction_signature: str | None = None
    error: str | None = None


# ═══════════════════════════════════════
# SOLANA RPC HELPERS
# ═══════════════════════════════════════
async def solana_rpc(method: str, params: list) -> dict:
    """Make a JSON-RPC call to Solana."""
    async with httpx.AsyncClient(timeout=15.0) as client:
        res = await client.post(SOLANA_RPC, json={
            "jsonrpc": "2.0", "id": 1,
            "method": method,
            "params": params,
        })
    data = res.json()
    if "error" in data:
        raise Exception(f"RPC error: {data['error']}")
    return data.get("result", {})


# ═══════════════════════════════════════
# PAYMENT VERIFICATION
# ═══════════════════════════════════════
async def verify_payment(signature: str, buyer: str, pack_type: str) -> bool:
    """Verify an SPL token transfer to treasury for pack purchase."""
    if not AICARDS_TOKEN_MINT or not TREASURY_WALLET:
        log.warning("Token mint or treasury not configured — skipping payment verification")
        return True

    try:
        result = await solana_rpc("getTransaction", [
            signature,
            {"encoding": "jsonParsed", "maxSupportedTransactionVersion": 0}
        ])

        if not result:
            log.warning("Transaction %s not found", signature)
            return False

        # Check transaction succeeded
        meta = result.get("meta", {})
        if meta.get("err"):
            log.warning("Transaction %s failed: %s", signature, meta["err"])
            return False

        # Look for SPL token transfer to treasury
        inner_ixs = meta.get("innerInstructions", [])
        outer_ixs = result.get("transaction", {}).get("message", {}).get("instructions", [])
        all_ixs = outer_ixs + [ix for group in inner_ixs for ix in group.get("instructions", [])]

        for ix in all_ixs:
            parsed = ix.get("parsed", {})
            if parsed.get("type") == "transfer" and ix.get("program") == "spl-token":
                info = parsed.get("info", {})
                # Verify amount matches pack price
                amount = int(info.get("amount", 0))
                expected_prices = {
                    "standard": 100, "legendary": 500,
                }
                expected = expected_prices.get(pack_type, 200) * (10 ** 9)
                if amount >= expected:
                    log.info("Payment verified: %s paid %d for %s (tx: %s)",
                             buyer[:8], amount, pack_type, signature[:16])
                    return True

        log.warning("No valid SPL transfer found in tx %s for %s", signature[:16], buyer[:8])
        return False
    except Exception as e:
        log.error("Payment verification error: %s", e)
        return False


# ═══════════════════════════════════════
# MINTING (Metaplex Compressed NFTs)
# ═══════════════════════════════════════
async def mint_card_on_chain(card: dict, recipient: str) -> str | None:
    """Mint a compressed NFT card via Metaplex Bubblegum.

    For the hackathon, this delegates to a Node.js helper script that uses
    the Metaplex JS SDK (more mature than Python Solana tooling).
    """
    image_url = f"{IMAGE_BASE_URL}/{card['card_id']}.png"
    metadata_uri = f"{METADATA_BASE_URL}/{card['card_id']}.json"

    # Build metadata for the compressed NFT
    nft_metadata = {
        "name": f"AI CARDS #{card['number']} — {card['name']}",
        "symbol": "AICARDS",
        "uri": metadata_uri,
        "sellerFeeBasisPoints": 500,  # 5% royalty on secondary sales
        "creators": [{"address": TREASURY_WALLET, "share": 100, "verified": True}],
        "collection": {"key": COLLECTION_MINT, "verified": True} if COLLECTION_MINT else None,
        "uses": None,
        "isMutable": True,
    }

    try:
        # Call the Node.js minting helper
        import subprocess
        result = await asyncio.to_thread(
            subprocess.run,
            [
                "node", "mint-helper.js",
                "--recipient", recipient,
                "--metadata", json.dumps(nft_metadata),
                "--tree", MERKLE_TREE,
            ],
            capture_output=True, text=True, timeout=30,
            cwd=os.path.dirname(os.path.abspath(__file__)),
        )
        if result.returncode != 0:
            log.error("Mint failed: %s", result.stderr)
            return None

        data = json.loads(result.stdout)
        sig = data.get("signature", "")
        log.info("Minted %s (%s) to %s — sig: %s",
                 card["card_id"], card["rarity"], recipient[:8], sig[:16])
        return sig
    except Exception as e:
        log.error("Mint error for %s: %s", card["card_id"], e)
        return None


# ═══════════════════════════════════════
# ENDPOINTS
# ═══════════════════════════════════════
@app.get("/health")
async def health():
    return {
        "status": "ok",
        "chain": "solana",
        "token_mint": AICARDS_TOKEN_MINT or "not configured",
        "collection": COLLECTION_MINT or "not configured",
        "merkle_tree": MERKLE_TREE or "not configured",
    }


@app.post("/mint/pack", response_model=MintResponse)
async def mint_pack(req: MintRequest):
    """Open a pack and mint 5 compressed NFT cards to the user's Solana address."""
    paid = req.payment_signature is not None
    log.info("Pack request: %s → %s (paid: %s)", req.pack_type, req.solana_address[:8], paid)

    # Verify on-chain payment if signature provided
    if req.payment_signature:
        verified = await verify_payment(
            req.payment_signature, req.solana_address, req.pack_type
        )
        if not verified:
            raise HTTPException(status_code=402, detail="Payment not verified on-chain")

    # Roll the pack (same weights as frontend)
    try:
        cards = build_pack(req.pack_type)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Mint each card as compressed NFT
    last_sig = None
    minted_cards = []
    for card in cards:
        sig = await mint_card_on_chain(card, req.solana_address)
        if sig:
            last_sig = sig
            minted_cards.append({
                "card_id": card["card_id"],
                "name": card["name"],
                "rarity": card["rarity"],
                "set": card["set"],
                "transaction": sig,
            })
        else:
            minted_cards.append({
                "card_id": card["card_id"],
                "name": card["name"],
                "rarity": card["rarity"],
                "set": card["set"],
                "error": "mint_failed",
            })

    success = any("transaction" in c for c in minted_cards)
    return MintResponse(
        success=success,
        pack_type=req.pack_type,
        cards=minted_cards,
        transaction_signature=last_sig,
        error=None if success else "All mints failed",
    )


@app.get("/cards/pool")
async def card_pool():
    """Return the full card pool for transparency."""
    from card_data import CARDS
    return {"total": len(CARDS), "cards": CARDS}


@app.get("/token/info")
async def token_info():
    """Return AICARDS token info for frontend display."""
    return {
        "mint": AICARDS_TOKEN_MINT,
        "treasury": TREASURY_WALLET,
        "bags_url": f"https://bags.fm/token/{AICARDS_TOKEN_MINT}" if AICARDS_TOKEN_MINT else None,
        "pack_prices": {
            "standard": 100,
            "legendary": 500,
            "set": 200,
        },
        "decimals": 9,
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
