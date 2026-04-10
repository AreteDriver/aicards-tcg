#!/usr/bin/env node
/**
 * AICARDS Token Launch on Bags Platform
 *
 * Launches the AICARDS token with 1B supply on Bags.fm with fee sharing config.
 * One-shot script — run once to create token and initial liquidity.
 *
 * Prerequisites:
 *   npm install @bagsfm/bags-sdk @solana/web3.js bs58 dotenv
 *
 * Environment variables (.env):
 *   BAGS_API_KEY        - API key from dev.bags.fm
 *   SOLANA_RPC_URL      - Helius/Quicknode mainnet RPC
 *   CREATOR_PRIVATE_KEY - Base58 encoded private key (launch wallet)
 *   TREASURY_WALLET     - (optional) Separate wallet for pack purchase revenue
 *   COMMUNITY_WALLET    - (optional) Wallet for community reward pool
 *
 * Usage:
 *   node scripts/launch-token.js
 */

import 'dotenv/config';
import { BagsSDK } from '@bagsfm/bags-sdk';
import { Connection, Keypair, PublicKey, VersionedTransaction } from '@solana/web3.js';
import bs58 from 'bs58';
import { readFileSync, writeFileSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));

// ── Config ──────────────────────────────────────────────────────────
const TOKEN_CONFIG = {
  name: 'AI CARDS',
  symbol: 'AICARDS',
  description:
    'The currency of survival in the age of AI displacement. ' +
    'Spend AICARDS to open card packs, battle raid bosses, and collect 448 cards ' +
    'across 19 sets in AI CARDS — 2030 Survival Edition. ' +
    'Every trade generates royalties that fund the game ecosystem. ' +
    'aicards.fun',
  website: 'https://aicards.fun',
  twitter: 'https://twitter.com/aicards_tcg',
  imageUrl: 'https://aicards.fun/og-image.png',
};

// Fee sharing: 70% treasury (game development), 30% community rewards
// Creator must be in the array per Bags rules. We split across wallets.
const FEE_SPLIT = {
  treasury: 7000,  // 70% — game development, server costs, new card sets
  community: 3000, // 30% — raid boss reward pools, tournament prizes, airdrops
};

// Initial buy: SOL amount for initial liquidity (in lamports)
const INITIAL_BUY_SOL = 1; // 1 SOL initial buy
const INITIAL_BUY_LAMPORTS = INITIAL_BUY_SOL * 1e9;

// ── Validation ──────────────────────────────────────────────────────
function validateEnv() {
  const required = ['BAGS_API_KEY', 'SOLANA_RPC_URL', 'CREATOR_PRIVATE_KEY'];
  const missing = required.filter((k) => !process.env[k]);
  if (missing.length > 0) {
    console.error('Missing environment variables:', missing.join(', '));
    console.error('Create a .env file in the project root. See script header for details.');
    process.exit(1);
  }
}

// ── Main ────────────────────────────────────────────────────────────
async function main() {
  validateEnv();

  const connection = new Connection(process.env.SOLANA_RPC_URL, 'processed');
  const sdk = new BagsSDK(process.env.BAGS_API_KEY, connection, 'processed');
  const keypair = Keypair.fromSecretKey(bs58.decode(process.env.CREATOR_PRIVATE_KEY));

  console.log('='.repeat(60));
  console.log('  AICARDS Token Launch on Bags');
  console.log('='.repeat(60));
  console.log(`  Creator wallet: ${keypair.publicKey.toBase58()}`);
  console.log(`  Token name:     ${TOKEN_CONFIG.name}`);
  console.log(`  Symbol:         ${TOKEN_CONFIG.symbol}`);
  console.log(`  Initial buy:    ${INITIAL_BUY_SOL} SOL`);
  console.log('='.repeat(60));

  // Check wallet balance
  const balance = await connection.getBalance(keypair.publicKey);
  const solBalance = balance / 1e9;
  console.log(`\n  Wallet balance: ${solBalance.toFixed(4)} SOL`);
  if (solBalance < INITIAL_BUY_SOL + 0.5) {
    console.error(`  Insufficient balance. Need at least ${INITIAL_BUY_SOL + 0.5} SOL (buy + fees).`);
    process.exit(1);
  }

  // Step 1: Create token metadata
  console.log('\n[1/4] Creating token metadata on Bags...');
  const metadataResponse = await sdk.tokenLaunch.createTokenInfoAndMetadata({
    name: TOKEN_CONFIG.name,
    symbol: TOKEN_CONFIG.symbol,
    description: TOKEN_CONFIG.description,
    imageUrl: TOKEN_CONFIG.imageUrl,
    website: TOKEN_CONFIG.website,
    twitter: TOKEN_CONFIG.twitter,
  });

  if (!metadataResponse.success) {
    console.error('Failed to create token metadata:', metadataResponse);
    process.exit(1);
  }

  const { tokenMint, tokenMetadata } = metadataResponse.response;
  console.log(`  Token mint:     ${tokenMint}`);
  console.log(`  Metadata URL:   ${tokenMetadata}`);

  // Step 2: Configure fee sharing
  console.log('\n[2/4] Configuring fee sharing...');

  const treasuryWallet = process.env.TREASURY_WALLET
    ? new PublicKey(process.env.TREASURY_WALLET)
    : keypair.publicKey;
  const communityWallet = process.env.COMMUNITY_WALLET
    ? new PublicKey(process.env.COMMUNITY_WALLET)
    : keypair.publicKey;

  // If treasury and community are the same wallet, combine BPS
  const feeClaimers =
    treasuryWallet.equals(communityWallet)
      ? [{ user: treasuryWallet, userBps: 10000 }]
      : [
          { user: treasuryWallet, userBps: FEE_SPLIT.treasury },
          { user: communityWallet, userBps: FEE_SPLIT.community },
        ];

  console.log('  Fee claimers:');
  feeClaimers.forEach((fc) =>
    console.log(`    ${fc.user.toBase58()}: ${fc.userBps / 100}%`)
  );

  const feeConfig = await sdk.config.createBagsFeeShareConfig({
    payer: keypair.publicKey,
    baseMint: new PublicKey(tokenMint),
    feeClaimers,
  });

  if (!feeConfig.success) {
    console.error('Failed to create fee config:', feeConfig);
    process.exit(1);
  }

  const { meteoraConfigKey, transactions: configTxs } = feeConfig.response;
  console.log(`  Config key:     ${meteoraConfigKey}`);
  console.log(`  Config txs:     ${configTxs.length}`);

  // Step 3: Create launch transaction
  console.log('\n[3/4] Creating launch transaction...');
  const launchTx = await sdk.tokenLaunch.createLaunchTransaction({
    metadataUrl: tokenMetadata,
    tokenMint: new PublicKey(tokenMint),
    launchWallet: keypair.publicKey,
    initialBuyLamports: INITIAL_BUY_LAMPORTS,
    configKey: new PublicKey(meteoraConfigKey),
  });

  // Step 4: Sign and submit everything
  console.log('\n[4/4] Signing and submitting transactions...');

  // Sign config transactions first
  const signedTxs = [];
  for (const txData of configTxs) {
    const tx = VersionedTransaction.deserialize(
      Buffer.from(txData.transaction, 'base64')
    );
    tx.sign([keypair]);
    signedTxs.push(tx);
  }

  // Sign launch transaction
  if (launchTx instanceof VersionedTransaction) {
    launchTx.sign([keypair]);
    signedTxs.push(launchTx);
  } else {
    // May already be serialized
    const tx = VersionedTransaction.deserialize(
      Buffer.from(launchTx, 'base64')
    );
    tx.sign([keypair]);
    signedTxs.push(tx);
  }

  // Submit via Jito bundle
  try {
    const bundleId = await sdk.solana.sendBundle(signedTxs);
    console.log(`  Bundle submitted: ${bundleId}`);

    // Poll for confirmation
    console.log('  Waiting for confirmation...');
    let confirmed = false;
    for (let i = 0; i < 30; i++) {
      await new Promise((r) => setTimeout(r, 2000));
      try {
        const statuses = await sdk.solana.getBundleStatuses([bundleId]);
        if (statuses?.[0]?.confirmation_status === 'confirmed' ||
            statuses?.[0]?.confirmation_status === 'finalized') {
          confirmed = true;
          break;
        }
      } catch {
        // Retry
      }
    }

    if (confirmed) {
      console.log('\n  TOKEN LAUNCHED SUCCESSFULLY!');
    } else {
      console.log('\n  Bundle submitted but confirmation timed out.');
      console.log('  Check on Solana explorer or bags.fm for status.');
    }
  } catch (err) {
    // Fallback: submit transactions individually via RPC
    console.log('  Bundle submission failed, trying direct RPC...');
    for (const tx of signedTxs) {
      const sig = await connection.sendTransaction(tx, {
        skipPreflight: false,
        maxRetries: 3,
      });
      console.log(`  TX submitted: ${sig}`);
      await connection.confirmTransaction(sig, 'confirmed');
      console.log(`  TX confirmed: ${sig}`);
    }
    console.log('\n  TOKEN LAUNCHED SUCCESSFULLY (via direct RPC)!');
  }

  // Save deployment info
  const deployInfo = {
    tokenMint,
    tokenMetadata,
    meteoraConfigKey,
    creatorWallet: keypair.publicKey.toBase58(),
    treasuryWallet: treasuryWallet.toBase58(),
    communityWallet: communityWallet.toBase58(),
    feeSplit: FEE_SPLIT,
    initialBuySOL: INITIAL_BUY_SOL,
    launchedAt: new Date().toISOString(),
    network: 'mainnet-beta',
    bagsUrl: `https://bags.fm/token/${tokenMint}`,
  };

  const deployPath = join(__dirname, 'deploy-info.json');
  writeFileSync(deployPath, JSON.stringify(deployInfo, null, 2));
  console.log(`\n  Deployment info saved to: ${deployPath}`);

  console.log('\n' + '='.repeat(60));
  console.log('  NEXT STEPS');
  console.log('='.repeat(60));
  console.log(`  1. Verify token on Bags: ${deployInfo.bagsUrl}`);
  console.log(`  2. Copy token mint to .env: AICARDS_TOKEN_MINT=${tokenMint}`);
  console.log('  3. Update index.html with token mint address');
  console.log('  4. Fund treasury wallet for pack reward distributions');
  console.log('='.repeat(60));
}

main().catch((err) => {
  console.error('Launch failed:', err);
  process.exit(1);
});
