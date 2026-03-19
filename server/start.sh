#!/bin/bash
# Setup Sui config from environment secrets before starting the server

SUI_CONFIG_DIR="/root/.sui/sui_config"
mkdir -p "$SUI_CONFIG_DIR"

# Write keystore from secret
if [ -n "$SUI_KEYSTORE" ]; then
    echo "$SUI_KEYSTORE" > "$SUI_CONFIG_DIR/sui.keystore"
fi

# Write client config
cat > "$SUI_CONFIG_DIR/client.yaml" << 'YAML'
---
keystore:
  File: /root/.sui/sui_config/sui.keystore
external_keys: ~
envs:
  - alias: testnet
    rpc: "https://fullnode.testnet.sui.io:443"
    ws: ~
    basic_auth: ~
    chain_id: 4c78adac
active_env: testnet
YAML

# Write aliases
cat > "$SUI_CONFIG_DIR/sui.aliases" << 'ALIASES'
[
  {
    "alias": "aicards-admin",
    "public_key_base64": "AI2bG3s5h/+Vrl6ll4Z3iuSPYpl04iem0SHfptJQYtSU"
  }
]
ALIASES

# Set active address
if [ -n "$SUI_ACTIVE_ADDRESS" ]; then
    echo "active_address: \"$SUI_ACTIVE_ADDRESS\"" >> "$SUI_CONFIG_DIR/client.yaml"
fi

echo "Sui config initialized"
sui client active-env 2>/dev/null || echo "Warning: Sui config check failed"

# Start server
exec uvicorn main:app --host 0.0.0.0 --port 8080
