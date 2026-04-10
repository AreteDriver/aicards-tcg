#!/bin/bash
# AI Cards Minting Server — Solana/Metaplex

echo "Starting AI Cards Minting API (Solana)"
echo "  RPC:        ${SOLANA_RPC_URL:-https://api.mainnet-beta.solana.com}"
echo "  Token mint: ${AICARDS_TOKEN_MINT:-not configured}"
echo "  Collection: ${AICARDS_COLLECTION_MINT:-not configured}"
echo "  Tree:       ${AICARDS_MERKLE_TREE:-not configured}"

# Verify Node.js minting helper is available
if [ -f "mint-helper.js" ]; then
    echo "  Mint helper: OK"
else
    echo "  WARNING: mint-helper.js not found — minting will fail"
fi

# Start server
exec uvicorn main:app --host 0.0.0.0 --port 8080
