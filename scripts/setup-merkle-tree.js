#!/usr/bin/env node
/**
 * Creates a Merkle tree for Metaplex Bubblegum compressed NFTs.
 *
 * Tree config: maxDepth=20, maxBufferSize=256 (supports ~1M mints, costs ~1.6 SOL)
 *
 * Usage:
 *   node scripts/setup-merkle-tree.js
 *
 * Outputs the tree address and authority PDA to add to server .env
 */

import 'dotenv/config';
import { createUmi } from '@metaplex-foundation/umi-bundle-defaults';
import { keypairIdentity, generateSigner } from '@metaplex-foundation/umi';
import { createTree } from '@metaplex-foundation/mpl-bubblegum';
import bs58 from 'bs58';

async function main() {
  const rpcUrl = process.env.SOLANA_RPC_URL;
  const creatorKey = process.env.CREATOR_PRIVATE_KEY;
  if (!rpcUrl || !creatorKey) {
    console.error('Set SOLANA_RPC_URL and CREATOR_PRIVATE_KEY in .env');
    process.exit(1);
  }

  const umi = createUmi(rpcUrl);
  const secretKey = bs58.decode(creatorKey);
  const signer = umi.eddsa.createKeypairFromSecretKey(secretKey);
  umi.use(keypairIdentity(signer));

  console.log('Creating Merkle tree for compressed NFTs...');
  console.log('  Max depth: 20 (~1M leaf nodes)');
  console.log('  Max buffer: 256');
  console.log('  Cost: ~1.6 SOL');

  const merkleTree = generateSigner(umi);

  const result = await createTree(umi, {
    merkleTree,
    maxDepth: 20,
    maxBufferSize: 256,
    public: false, // Only tree authority (our server) can mint
  }).sendAndConfirm(umi);

  console.log('\n  Merkle tree created!');
  console.log(`  Tree address:    ${merkleTree.publicKey}`);
  console.log(`  TX signature:    ${bs58.encode(result.signature)}`);
  console.log('\n  Add to server .env:');
  console.log(`  AICARDS_MERKLE_TREE=${merkleTree.publicKey}`);
}

main().catch(err => {
  console.error('Failed:', err);
  process.exit(1);
});
