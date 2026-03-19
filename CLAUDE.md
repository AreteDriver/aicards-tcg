# CLAUDE.md — aicards-tcg

## Project Overview

AI CARDS — 2030 Survival Edition. A collectible card experience about AI displacement and the humans who survive automation. Gacha-style pack opening with 118 cards across 6 rarities and 4 sets. Cards are NFTs on Sui blockchain — tradeable, sellable, collectible on-chain. Live at **aicards.fun**.

## Current State

- **Stack**: Single HTML file (CSS + vanilla JS) + Sui Move contracts
- **Hosting**: Vercel (auto-deploy from GitHub main branch)
- **Domain**: aicards.fun (Vercel DNS)
- **Cards**: 118 total across 4 sets, 6 rarities (MYTHIC, LEGENDARY, RARE, UNCOMMON, COMMON, JUNK)
- **Blockchain**: Sui testnet — Package `0x848b7e822fc93e05212d0002287d079d3cb5ef7fe0be1458091496aaf2aa95d2`
- **On-chain objects**: AdminCap `0xb8fca933e7198d496f75027f6a0d3189dcd3651205a5f6f590ee2571837cada3`

## Architecture

```
aicards-tcg/
├── index.html                  # The entire frontend — CSS, JS, card data, all inline
├── contracts/aicards/          # Sui Move smart contracts
│   ├── Move.toml               # Package manifest
│   ├── sources/card.move       # Card NFT, AdminCap, mint, mint_pack, burn
│   └── tests/card_tests.move   # 4 tests (init, mint, burn, transfer/trade)
├── og-image.html               # Source file for OG social preview image
├── og-image.png                # Generated 1200x630 social preview
├── CLAUDE.md                   # This file
└── .gitignore
```

## Sets & Card Counts

| Set | Series Key | Cards | Mythics | Unlock Condition |
|-----|-----------|-------|---------|-----------------|
| 2030 Survival | (none) | 49 | 0 | Always open |
| Jobless.ai | `jobless` | 25 | 5 | Set 1 100% complete |
| DOOMSCROLL | `doomscroll` | 22 | 5 | Set 2 100% complete |
| LOVE.EXE | `loveexe` | 22 | 5 | Set 3 100% complete |

## Pack Types

| Pack | Set | Description |
|------|-----|-------------|
| 2030 SURVIVAL | Set 1 | Full pool, weighted by rarity |
| REDUNDANCY | Set 1 | 1 Legendary guaranteed + 4 weighted |
| JOBLESS.AI | Set 2 | All jobless series cards, weighted |
| DOOMSCROLL | Set 3 | All doomscroll series cards, weighted |
| LOVE.EXE | Set 4 | All loveexe series cards, weighted |

## Rarity Weights (per card slot)

MYTHIC: 1, LEGENDARY: 300, RARE: 1000, UNCOMMON: 2200, COMMON: 4000, JUNK: 2500
(MYTHIC ≈ 1/10,000 per slot, ∞/∞ ATK/DEF)

## Common Commands

```bash
# Deploy frontend (auto on push, or manual)
vercel --prod

# Validate JS syntax
node -e "const h=require('fs').readFileSync('index.html','utf8');const s=h.match(/<script>([\s\S]*?)<\/script>/);new Function(s[1]);console.log('OK')"

# Count cards
grep -c 'rarity:"' index.html

# Build Move contracts
cd contracts/aicards && sui move build

# Test Move contracts
cd contracts/aicards && sui move test

# Deploy Move contracts (testnet)
cd contracts/aicards && sui client publish --gas-budget 100000000

# Run anchormd audit
anchormd audit CLAUDE.md
```

## Domain Context

This is a social commentary piece disguised as a card game. The tone is dark humor — laugh then cry. Cards represent real roles affected by AI automation. The "Karpathy Score" (0-10) measures AI displacement risk. Each card has a named satirical ability (e.g., ⚡ HOUSE CALL, ⚡ DEPRECATED).

**Card rarities map to survival odds:**
- Mythic (prismatic/rainbow) — The jobs AI literally cannot take (1/10,000 pull rate, ∞/∞)
- Legendary (gold) — Trades that cannot be automated (plumber, welder, etc.)
- Rare (purple) — Human purpose roles that resist automation (therapist, nurse, etc.)
- Uncommon (blue) — Society roles being displaced (journalist, accountant, etc.)
- Common (pink) — AI products replacing human connection (AI girlfriend, dating algo, etc.)
- Junk (gray) — Lore characters and meta-commentary (VC, LinkedIn guru, etc.)

## Gameplay Systems

- **Daily packs**: 5 free per day, resets at midnight
- **Daily missions**: Open 5 packs, Pull Legendary, Pull 3 rarities, Share card
- **Weekly goal**: Complete all daily missions 7 days → 1 free Jobless.ai pack
- **Pity system**: Guaranteed Legendary after 10 packs without one
- **Progressive unlock**: Each set gates behind previous set's 100% completion
- **Survival profile**: Sovereignty vs Dependency based on card pulls

## Sui Integration

- **Non-intrusive**: Wallet CTA appears after 2+ packs opened, dismissable
- **Address-based**: Users paste Sui address (no extension required, mobile-friendly)
- **Trading**: Cards have `store` ability — native Sui transfers + Kiosk marketplace compatible
- **Mint flow**: Server-side minting via AdminCap (rarity determined server-side)

## Dependencies

- **Google Fonts**: Cinzel, Cinzel Decorative, IM Fell English, Share Tech Mono
- **html2canvas**: v1.4.1 CDN — card screenshot/share feature
- **Vercel Analytics**: Speed insights + page analytics
- **Web Audio API**: Procedural sound effects (no external audio files)
- **Sui Move**: Framework testnet rev

## Coding Standards

- **Single file**: All CSS, JS, and HTML live in index.html. No build step. Keep it that way.
- **Naming**: camelCase for JS, kebab-case for CSS classes, kebab-case for card IDs
- **Card data**: Each card is a JS object in the CARDS array with `series` field for set membership
- **CSS art**: Each card gets an `.art-{id}` class with `::before` (background pattern) and `::after` (emoji icon)
- **Rarity colors**: Use CSS variables (--gold, --purple, --blue, --pink, --gray) + white for MYTHIC
- **State**: localStorage key `aicards2_state`, collection stored as `{cardId: count}` object
- **Set filtering**: `pickCard()` filters by `!c.series` for Set 1; set-specific packs filter by `c.series===type`

## Anti-Patterns (Do NOT Do)

- Do NOT split frontend into multiple files — the single-file architecture is intentional
- Do NOT add a build step, bundler, or framework to the frontend
- Do NOT use external image assets — all art is CSS-only with emoji overlays
- Do NOT make the tone preachy or moralistic — it should make you laugh, then make you sad
- Do NOT hardcode card counts in HTML — derive from CARDS.length in JS
- Do NOT force wallet connection — let users play first, offer chain integration naturally

## Git Conventions

- Commit messages: Conventional commits (`feat:`, `fix:`, `chore:`)
- Push to main triggers Vercel auto-deploy
- Validate JS syntax before committing
