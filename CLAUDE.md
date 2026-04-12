# CLAUDE.md — aicards-tcg

## Project Overview

AI CARDS — 2030 Survival Edition. A collectible card experience about AI displacement and the humans who survive automation. Gacha-style pack opening with 448 cards across 6 rarities and 19 sets. Cards are NFTs on Sui blockchain — tradeable, sellable, collectible on-chain. Minting API live. Live at **aicards.fun**.

## Current State

- **Stack**: Single HTML file (CSS + vanilla JS) + Sui Move contracts + Next.js admin
- **Hosting**: Vercel (frontend, auto-deploy) + Fly.io (admin dashboard + minting API + Postgres)
- **Domain**: aicards.fun (Vercel DNS)
- **Cards**: 448 total across 19 sets, 6 rarities (MYTHIC, LEGENDARY, RARE, UNCOMMON, COMMON, JUNK)
- **Card art**: 448/448 cards have DALL-E 3 generated PNG art (black & white underground comix style)
- **Blockchain**: Sui testnet — Package `0x99f91c55ad24367b9fba1000bf43a5e571c2ae096c906fdf2e78fd51243f38b2`
- **On-chain objects**: AdminCap `0xcfeaad94ff0f5136b037f3482ff68fc00cacc5149b3db8dfe011e239644e4935`
- **Minting API**: `https://aicards-mint.fly.dev` (FastAPI on Fly.io, 448 cards)

## Architecture

```
aicards-tcg/
├── index.html                  # The entire frontend — CSS, JS, card data, all inline
├── lang/                       # i18n translations (6 languages)
│   ├── en.json                 # English (default, 250+ keys)
│   ├── ja.json / ko.json       # Japanese, Korean
│   ├── es.json / pt.json       # Spanish, Portuguese
│   └── zh.json                 # Chinese (Simplified)
├── images/cards/               # 448 DALL-E 3 card art PNGs (b&w comix style)
├── images/generate_cards.py    # DALL-E 3 batch art generator
├── contracts/aicards/          # Sui Move smart contracts
│   ├── Move.toml               # Package manifest
│   ├── sources/card.move       # Card NFT, AdminCap, mint, mint_pack, burn
│   ├── sources/payment.move    # Treasury, buy_pack (SUI payment), withdraw, set_price
│   ├── tests/card_tests.move   # 4 tests (init, mint, burn, transfer/trade)
│   └── tests/payment_tests.move # 5 tests (buy, change, withdraw, price, auth)
├── server/                     # Minting API (FastAPI on Fly.io)
│   ├── main.py                 # POST /mint/pack, GET /health, GET /cards/pool
│   ├── card_data.py            # All 448 cards with rarity weights
│   ├── Dockerfile              # Python 3.12 + Sui CLI binary
│   ├── fly.toml                # Fly.io config (aicards-mint)
│   └── start.sh                # Sui keystore injection from secrets
├── admin/                      # Admin dashboard (Next.js on Fly.io)
│   ├── app/page.tsx            # Dashboard UI (wallet login + metrics)
│   ├── app/providers.tsx       # dapp-kit SuiClientProvider + WalletProvider
│   ├── app/api/admin/          # Auth + metrics API routes
│   ├── app/api/events/         # Event logging endpoints (pack/pull/raid/share)
│   ├── lib/adminAuth.ts        # Sui zkLogin signature verification + JWT
│   ├── lib/db.ts               # PostgreSQL connection pool
│   ├── lib/metrics.ts          # Dashboard query helpers
│   ├── db/schema.sql           # 7 metrics tables
│   ├── Dockerfile              # Next.js standalone on Fly.io
│   └── fly.toml                # Fly.io config (aicards-admin)
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
| FOUNDER.EXE | `founderexe` | 22 | 5 | Set 6 100% complete |
| DEEPSTATE.AI | `deepstateai` | 22 | 5 | Set 7 100% complete |
| HEALTHCARE.SYS | `healthcaresys` | 22 | 5 | Set 8 100% complete |
| PARENT.TRAP | `parenttrap` | 22 | 5 | Set 9 100% complete |
| CLIMATE.ERR | `climateerr` | 22 | 5 | Set 10 100% complete |
| CREATOR.NULL | `creatornull` | 22 | 5 | Set 11 100% complete |
| ANALOG.REVIVAL | `analogrevival` | 22 | 5 | Set 12 100% complete |
| MERGE.PROTOCOL | `mergeprotocol` | 22 | 5 | Set 13 100% complete |
| UBI.WORLD | `ubiworld` | 22 | 5 | Set 14 100% complete |
| WALLED.GARDEN | `walledgarden` | 22 | 5 | Set 15 100% complete |
| SOLARPUNK.SYS | `solarpunk` | 22 | 5 | Set 16 100% complete |
| GREY.ZONE | `greyzone` | 22 | 5 | Set 17 100% complete |
| FRONTIER.NULL | `frontiernull` | 22 | 5 | Set 18 100% complete |

## Pack Types

All packs contain **10 cards**. The former REDUNDANCY (5-card, 1 Legendary guaranteed) lane was removed when packs grew to 10 — a 10-card weighted pull already makes a Legendary likely, so the guaranteed lane was redundant.

| Pack | Set | Description |
|------|-----|-------------|
| 2030 SURVIVAL | Set 1 | Full pool, weighted by rarity |
| JOBLESS.AI | Set 2 | All jobless series cards, weighted |
| DOOMSCROLL | Set 3 | All doomscroll series cards, weighted |
| LOVE.EXE | Set 4 | All loveexe series cards, weighted |
| WAR ROOM | Set 5 | All warroom series cards, weighted |
| SKILLS.VOID | Set 6 | All skillsvoid series cards, weighted |
| FOUNDER.EXE | Set 7 | Startup carnage series cards, weighted |
| DEEP STATE AI | Set 8 | Surveillance state series cards, weighted |
| HEALTHCARE.SYS | Set 9 | Medical dystopia series cards, weighted |
| PARENT TRAP | Set 10 | Digital childhood series cards, weighted |
| CLIMATE.ERR | Set 11 | Planetary debt series cards, weighted |
| CREATOR.NULL | Set 12 | Creative extinction series cards, weighted |
| ANALOG.REVIVAL | Set 13 | Analog backlash world, hand-made luxury |
| MERGE.PROTOCOL | Set 14 | Neural integration, human-AI merge |
| UBI.WORLD | Set 15 | Post-work, meaning crisis |
| WALLED.GARDEN | Set 16 | Corporate consolidation, GAM owns all |
| SOLARPUNK.SYS | Set 17 | Optimistic future, utopia cracks |
| GREY.ZONE | Set 18 | Surveillance state, resistance |
| FRONTIER.NULL | Set 19 | Mars colony, humans as cargo |

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

- **Free packs**: 3 free per hour, refreshes with each raid boss rotation (top of the UTC hour). Pack size is **10 cards** (see `PACK_SIZE` constant in both `index.html` and `server/card_data.py`).
- **Pack types**: Survival (weighted full-pool) + one per expansion set. The former "REDUNDANCY" legendary-guaranteed lane was removed — 10-card packs make it redundant.
- **Daily missions**: Open packs, Pull Legendary, Pull 3 rarities, Share card
- **Weekly goal**: Complete all daily missions 7 days → 1 free Jobless.ai pack
- **Pity system**: Guaranteed Legendary after 5 packs without one (lowered from 10 when packs grew to 10 cards)
- **Progressive unlock**: Each set gates behind previous set's 100% completion
- **Survival profile**: Sovereignty vs Dependency based on card pulls
- **Raid Boss battles**: Hourly rotating bosses (12 total, 3 tiers), 5-card team selection, turn-based auto-combat
  - Damage formula: BaseATK × RarityMult × CategoryBonus × AntiKarpathy
  - Set bonus (3+ same set = ×1.5), Solidarity combo (Human Trade + Human Purpose = ×1.25)
  - Milestones at 25%/50%/75% boss HP for bonus reward packs
  - 5 attempts per boss, reward packs bypass the hourly free-pack limit
  - Boss rotation: hourly, UTC hour % 12, APEX at US peak hours. Free-pack budget and countdown timer are keyed to the same rotation so they refresh in lockstep.

## Internationalization (i18n)

- **Languages**: EN, JA, KO, ES, PT, ZH
- **Engine**: `t(key, ...args)` for UI, `cardT(cardId, field)` for cards, `rarityT()`, `catT()`
- **Files**: `lang/{locale}.json` — loaded via fetch on demand, EN is default
- **Persistence**: `localStorage` key `aicards_lang`, browser locale detection as fallback
- **Scope**: Full i18n — 300+ UI strings + 448 card translations (name, category, stat labels, flavor text) per language
- **Selector**: Top-left corner, 6 language buttons

## Sui Integration

- **Non-intrusive**: Wallet CTA appears after 2+ packs opened, dismissable
- **Address-based**: Users paste Sui address (no extension required, mobile-friendly)
- **Trading**: Cards have `store` ability — native Sui transfers + Kiosk marketplace compatible
- **Mint flow**: Server-side minting via AdminCap (rarity determined server-side)
- **Payment**: Treasury shared object, buy_pack() accepts SUI, change returned on overpay
- **Minting API**: `aicards-mint.fly.dev` — POST /mint/pack, 448 cards, all 19 sets
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
- Do NOT use external image CDNs — card art PNGs live in images/cards/, CSS art is emoji fallback
- Do NOT make the tone preachy or moralistic — it should make you laugh, then make you sad
- Do NOT hardcode card counts in HTML — derive from CARDS.length in JS
- Do NOT force wallet connection — let users play first, offer chain integration naturally

## Git Conventions

- Commit messages: Conventional commits (`feat:`, `fix:`, `chore:`)
- Push to main triggers Vercel auto-deploy
- Validate JS syntax before committing
