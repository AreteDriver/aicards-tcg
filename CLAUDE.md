# CLAUDE.md — aicards-tcg

## Project Overview

AI CARDS — 2030 Survival Edition. A collectible card experience about AI displacement and the humans who survive automation. Gacha-style pack opening with 162 cards across 6 rarities and 6 sets. Cards are NFTs on Sui blockchain — tradeable, sellable, collectible on-chain. Minting API live. Live at **aicards.fun**.

## Current State

- **Stack**: Single HTML file (CSS + vanilla JS) + Sui Move contracts
- **Hosting**: Vercel (auto-deploy from GitHub main branch)
- **Domain**: aicards.fun (Vercel DNS)
- **Cards**: 162 total across 6 sets, 6 rarities (MYTHIC, LEGENDARY, RARE, UNCOMMON, COMMON, JUNK)
- **Blockchain**: Sui testnet — Package `0x99f91c55ad24367b9fba1000bf43a5e571c2ae096c906fdf2e78fd51243f38b2`
- **On-chain objects**: AdminCap `0xcfeaad94ff0f5136b037f3482ff68fc00cacc5149b3db8dfe011e239644e4935`
- **Minting API**: `https://aicards-mint.fly.dev` (FastAPI on Fly.io, 162 cards)

## Architecture

```
aicards-tcg/
├── index.html                  # The entire frontend — CSS, JS, card data, all inline
├── contracts/aicards/          # Sui Move smart contracts
│   ├── Move.toml               # Package manifest
│   ├── sources/card.move       # Card NFT, AdminCap, mint, mint_pack, burn
│   ├── sources/payment.move    # Treasury, buy_pack (SUI payment), withdraw, set_price
│   ├── tests/card_tests.move   # 4 tests (init, mint, burn, transfer/trade)
│   └── tests/payment_tests.move # 5 tests (buy, change, withdraw, price, auth)
├── server/                     # Minting API (FastAPI on Fly.io)
│   ├── main.py                 # POST /mint/pack, GET /health, GET /cards/pool
│   ├── card_data.py            # All 162 cards with rarity weights
│   ├── Dockerfile              # Python 3.12 + Sui CLI binary
│   ├── fly.toml                # Fly.io config (aicards-mint)
│   └── start.sh                # Sui keystore injection from secrets
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
| WAR ROOM | `warroom` | 22 | 5 | Set 4 100% complete |
| SKILLS.VOID | `skillsvoid` | 22 | 5 | Set 5 100% complete |

## Pack Types

| Pack | Set | Description |
|------|-----|-------------|
| 2030 SURVIVAL | Set 1 | Full pool, weighted by rarity |
| REDUNDANCY | Set 1 | 1 Legendary guaranteed + 4 weighted |
| JOBLESS.AI | Set 2 | All jobless series cards, weighted |
| DOOMSCROLL | Set 3 | All doomscroll series cards, weighted |
| LOVE.EXE | Set 4 | All loveexe series cards, weighted |
| WAR ROOM | Set 5 | All warroom series cards, weighted |
| SKILLS.VOID | Set 6 | All skillsvoid series cards, weighted |

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
- **Raid Boss battles**: Weekly rotating bosses (8 total), 5-card team selection, turn-based auto-combat
  - Damage formula: BaseATK × RarityMult × CategoryBonus × AntiKarpathy
  - Set bonus (3+ same set = ×1.5), Solidarity combo (Human Trade + Human Purpose = ×1.25)
  - Milestones at 25%/50%/75% boss HP for bonus reward packs
  - 3 daily attempts, reward packs bypass daily limit
  - Boss rotation: weekly, deterministic seed from Date.now()

## Internationalization (i18n)

- **Languages**: EN, JA, KO, ES, PT, ZH
- **Engine**: `t(key, ...args)` for UI, `cardT(cardId, field)` for cards, `rarityT()`, `catT()`
- **Files**: `lang/{locale}.json` — loaded via fetch on demand, EN is default
- **Persistence**: `localStorage` key `aicards_lang`, browser locale detection as fallback
- **Scope**: Full i18n — 210+ UI strings + 162 card translations (name, category, stat labels, flavor text) per language
- **Selector**: Top-left corner, 6 language buttons

## Sui Integration

- **Non-intrusive**: Wallet CTA appears after 2+ packs opened, dismissable
- **Address-based**: Users paste Sui address (no extension required, mobile-friendly)
- **Trading**: Cards have `store` ability — native Sui transfers + Kiosk marketplace compatible
- **Mint flow**: Server-side minting via AdminCap (rarity determined server-side)
- **Payment**: Treasury shared object, buy_pack() accepts SUI, change returned on overpay
- **Minting API**: `aicards-mint.fly.dev` — POST /mint/pack, 162 cards, all 6 sets
- **Move tests**: 9 passing (4 card + 5 payment)

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
