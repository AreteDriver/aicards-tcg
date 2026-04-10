#!/usr/bin/env node
/**
 * Metaplex Bubblegum minting helper — called by the Python FastAPI server.
 *
 * Mints a single compressed NFT to a recipient address using an existing Merkle tree.
 *
 * Usage:
 *   node mint-helper.js --recipient <address> --metadata <json> --tree <address>
 *
 * Environment:
 *   SOLANA_RPC_URL       - Solana RPC endpoint
 *   AICARDS_CREATOR_KEYPAIR - Base58 encoded private key
 *
 * Outputs JSON to stdout: { signature: "..." }
 */

import { Connection, Keypair, PublicKey } from '@solana/web3.js';
import { createUmi } from '@metaplex-foundation/umi-bundle-defaults';
import { keypairIdentity } from '@metaplex-foundation/umi';
import { mintToCollectionV1 } from '@metaplex-foundation/mpl-bubblegum';
import { publicKey as umiPublicKey } from '@metaplex-foundation/umi';
import bs58 from 'bs58';

function parseArgs() {
  const args = process.argv.slice(2);
  const result = {};
  for (let i = 0; i < args.length; i += 2) {
    result[args[i].replace('--', '')] = args[i + 1];
  }
  return result;
}

async function main() {
  const args = parseArgs();
  if (!args.recipient || !args.metadata || !args.tree) {
    console.error(JSON.stringify({ error: 'Missing required args: --recipient --metadata --tree' }));
    process.exit(1);
  }

  const rpcUrl = process.env.SOLANA_RPC_URL || 'https://api.mainnet-beta.solana.com';
  const creatorKey = process.env.AICARDS_CREATOR_KEYPAIR;
  if (!creatorKey) {
    console.error(JSON.stringify({ error: 'AICARDS_CREATOR_KEYPAIR not set' }));
    process.exit(1);
  }

  const metadata = JSON.parse(args.metadata);

  // Initialize Umi with Metaplex
  const umi = createUmi(rpcUrl);
  const secretKey = bs58.decode(creatorKey);
  const signer = umi.eddsa.createKeypairFromSecretKey(secretKey);
  umi.use(keypairIdentity(signer));

  const merkleTree = umiPublicKey(args.tree);
  const leafOwner = umiPublicKey(args.recipient);

  try {
    const result = await mintToCollectionV1(umi, {
      leafOwner,
      merkleTree,
      collectionMint: metadata.collection?.key
        ? umiPublicKey(metadata.collection.key)
        : undefined,
      metadata: {
        name: metadata.name,
        symbol: metadata.symbol || 'AICARDS',
        uri: metadata.uri,
        sellerFeeBasisPoints: metadata.sellerFeeBasisPoints || 500,
        collection: metadata.collection
          ? { key: umiPublicKey(metadata.collection.key), verified: false }
          : null,
        creators: (metadata.creators || []).map(c => ({
          address: umiPublicKey(c.address),
          verified: false,
          share: c.share,
        })),
      },
    }).sendAndConfirm(umi);

    const signature = bs58.encode(result.signature);
    console.log(JSON.stringify({ signature }));
  } catch (err) {
    console.error(JSON.stringify({ error: err.message || String(err) }));
    process.exit(1);
  }
}

main();
