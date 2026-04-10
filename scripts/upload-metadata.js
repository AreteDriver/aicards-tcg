#!/usr/bin/env node
/**
 * Generates and uploads Metaplex-compatible metadata JSON for all 448 cards.
 *
 * Creates metadata files at public/metadata/{card_id}.json matching Metaplex standard.
 * For hackathon: serves from aicards.fun/metadata/ via Vercel static.
 * For production: upload to Arweave via Irys.
 *
 * Usage:
 *   node scripts/upload-metadata.js
 */

import { readFileSync, writeFileSync, mkdirSync, existsSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = join(__dirname, '..');

// Extract card data from index.html (parse the CARDS array)
function extractCards() {
  const html = readFileSync(join(ROOT, 'index.html'), 'utf8');

  // Find all _add() calls in card_data.py instead (more reliable)
  const cardDataPy = readFileSync(join(ROOT, 'server', 'card_data.py'), 'utf8');
  const cards = [];

  // Match _add("id", "name", "rarity", "category", "set", "kscore", "atk", "def", "symbol" ...)
  const addPattern = /_add\("([^"]+)",\s*"([^"]+)",\s*"([^"]+)",\s*"([^"]+)",\s*"([^"]+)",\s*"([^"]*)",\s*"([^"]*)",\s*"([^"]*)",\s*"([^"]*)"/g;
  let match;
  let number = 0;
  while ((match = addPattern.exec(cardDataPy)) !== null) {
    number++;
    cards.push({
      card_id: match[1],
      name: match[2],
      rarity: match[3],
      category: match[4],
      set: match[5],
      kscore: match[6],
      atk: match[7],
      def: match[8],
      symbol: match[9],
      number,
    });
  }

  return cards;
}

function generateMetadata(card) {
  const rarityColors = {
    MYTHIC: 'Prismatic',
    LEGENDARY: 'Gold',
    RARE: 'Purple',
    UNCOMMON: 'Blue',
    COMMON: 'Pink',
    JUNK: 'Gray',
  };

  return {
    name: `AI CARDS #${card.number} — ${card.name}`,
    symbol: 'AICARDS',
    description: `${card.name} — ${card.category} from ${card.set}. Karpathy Score: ${card.kscore}/10. ATK: ${card.atk} | DEF: ${card.def}. AI CARDS — 2030 Survival Edition.`,
    image: `https://aicards.fun/images/cards/${card.card_id}.png`,
    external_url: 'https://aicards.fun',
    attributes: [
      { trait_type: 'Rarity', value: card.rarity },
      { trait_type: 'Category', value: card.category },
      { trait_type: 'Set', value: card.set },
      { trait_type: 'Karpathy Score', value: card.kscore },
      { trait_type: 'ATK', value: card.atk },
      { trait_type: 'DEF', value: card.def },
      { trait_type: 'Card Number', value: card.number.toString() },
      { trait_type: 'Rarity Color', value: rarityColors[card.rarity] || 'Unknown' },
    ],
    properties: {
      files: [
        {
          uri: `https://aicards.fun/images/cards/${card.card_id}.png`,
          type: 'image/png',
        },
      ],
      category: 'image',
      creators: [
        {
          address: '', // Set to treasury wallet after token launch
          share: 100,
        },
      ],
    },
    collection: {
      name: 'AI CARDS — 2030 Survival Edition',
      family: 'AI CARDS',
    },
    seller_fee_basis_points: 500, // 5% royalty
  };
}

function main() {
  const cards = extractCards();
  console.log(`Found ${cards.length} cards in card_data.py`);

  const metadataDir = join(ROOT, 'metadata');
  if (!existsSync(metadataDir)) mkdirSync(metadataDir, { recursive: true });

  let count = 0;
  for (const card of cards) {
    const metadata = generateMetadata(card);
    const path = join(metadataDir, `${card.card_id}.json`);
    writeFileSync(path, JSON.stringify(metadata, null, 2));
    count++;
  }

  console.log(`Generated ${count} metadata files in ${metadataDir}/`);
  console.log('\nMetadata will be served from: https://aicards.fun/metadata/{card_id}.json');
  console.log('Add a rewrite rule in vercel.json if needed.');

  // Summary by rarity
  const byRarity = {};
  cards.forEach(c => { byRarity[c.rarity] = (byRarity[c.rarity] || 0) + 1; });
  console.log('\nRarity breakdown:');
  Object.entries(byRarity).sort((a, b) => b[1] - a[1]).forEach(([r, n]) => {
    console.log(`  ${r}: ${n}`);
  });
}

main();
