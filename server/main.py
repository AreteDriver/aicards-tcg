"""AI Cards Minting API — mints NFT cards on Sui via AdminCap."""

import asyncio
import json
import logging
import os
import re
import subprocess

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, field_validator

from card_data import build_pack

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("aicards")

# ═══════════════════════════════════════
# CONFIG
# ═══════════════════════════════════════
PACKAGE_ID = os.getenv(
    "AICARDS_PACKAGE_ID",
    "0x99f91c55ad24367b9fba1000bf43a5e571c2ae096c906fdf2e78fd51243f38b2",
)
ADMIN_CAP_ID = os.getenv(
    "AICARDS_ADMIN_CAP_ID",
    "0xcfeaad94ff0f5136b037f3482ff68fc00cacc5149b3db8dfe011e239644e4935",
)
SUI_BIN = os.getenv("SUI_BIN", "sui")
GAS_BUDGET = "50000000"  # 0.05 SUI per mint
IMAGE_BASE_URL = os.getenv("AICARDS_IMAGE_URL", "https://aicards.fun/cards")

VALID_PACK_TYPES = {"standard", "legendary", "jobless", "doomscroll", "loveexe", "warroom", "skillsvoid"}

# ═══════════════════════════════════════
# APP
# ═══════════════════════════════════════
app = FastAPI(title="AI Cards Minting API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://aicards.fun", "http://localhost:3000", "http://localhost:8000"],
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)


class MintRequest(BaseModel):
    sui_address: str
    pack_type: str

    @field_validator("sui_address")
    @classmethod
    def validate_address(cls, v: str) -> str:
        v = v.strip()
        if not re.match(r"^0x[a-fA-F0-9]{64}$", v):
            raise ValueError("Invalid Sui address — must be 0x + 64 hex chars")
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
    transaction_digest: str | None = None
    error: str | None = None


# ═══════════════════════════════════════
# MINTING
# ═══════════════════════════════════════
async def mint_card_on_chain(card: dict, recipient: str) -> str | None:
    """Mint a single card NFT via `sui client call`."""
    image_url = f"{IMAGE_BASE_URL}/{card['card_id']}.png"

    cmd = [
        SUI_BIN, "client", "call",
        "--package", PACKAGE_ID,
        "--module", "card",
        "--function", "mint",
        "--args",
        ADMIN_CAP_ID,
        card["card_id"],
        card["name"],
        card["rarity"],
        card["category"],
        card["set"],
        card["kscore"],
        card["atk"],
        card["def"],
        card.get("flavor", ""),
        card["symbol"],
        str(card["number"]),
        image_url,
        recipient,
        "--gas-budget", GAS_BUDGET,
        "--json",
    ]

    try:
        result = await asyncio.to_thread(
            subprocess.run, cmd, capture_output=True, text=True, timeout=30
        )
        if result.returncode != 0:
            log.error("Mint failed: %s", result.stderr)
            return None

        data = json.loads(result.stdout)
        digest = data.get("digest", "")
        log.info("Minted %s (%s) to %s — tx: %s", card["card_id"], card["rarity"], recipient[:10], digest)
        return digest
    except Exception as e:
        log.error("Mint error: %s", e)
        return None


# ═══════════════════════════════════════
# ENDPOINTS
# ═══════════════════════════════════════
@app.get("/health")
async def health():
    return {"status": "ok", "package": PACKAGE_ID}


@app.post("/mint/pack", response_model=MintResponse)
async def mint_pack(req: MintRequest):
    """Open a pack and mint 5 cards to the user's Sui address."""
    log.info("Pack request: %s → %s", req.pack_type, req.sui_address[:10])

    # Roll the pack (same weights as frontend)
    try:
        cards = build_pack(req.pack_type)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Mint each card on-chain
    last_digest = None
    minted_cards = []
    for card in cards:
        digest = await mint_card_on_chain(card, req.sui_address)
        if digest:
            last_digest = digest
            minted_cards.append({
                "card_id": card["card_id"],
                "name": card["name"],
                "rarity": card["rarity"],
                "set": card["set"],
                "transaction": digest,
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
        transaction_digest=last_digest,
        error=None if success else "All mints failed",
    )


@app.get("/cards/pool")
async def card_pool():
    """Return the full card pool for transparency."""
    from card_data import CARDS
    return {"total": len(CARDS), "cards": CARDS}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
