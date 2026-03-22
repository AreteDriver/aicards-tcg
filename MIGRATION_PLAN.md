# aicards-tcg → crypto-cards Migration Plan

## Status: PLANNING (not started)

## Overview

Migrate aicards-tcg from a single-file vanilla JS app into the `crypto-cards` pnpm monorepo as `packages/aicards`. This enables code reuse via the shared `@crypto-cards/shared` card engine across all card game variants.

## Current Architecture

- **aicards-tcg**: Single `index.html` (~10K lines CSS+JS), no build step, vanilla JS
- **crypto-cards**: React 19 + Vite pnpm monorepo, 3 packages (shared, rug-museum, sui-ecosystem)
- **Shared engine**: `CardEngine` (gacha pull), `Gallery` (collection view), `PullAnimation`, rarity weights

## What Migrates vs What's Unique

### Can use shared engine:
- Card pulling/reveal animation → `CardEngine`
- Collection gallery → `Gallery`
- Rarity weights → `weightedPull()`
- Card back styling → `CardBack`

### Unique to aicards (must be custom):
- 294 cards with full metadata (stats, flavor, Karpathy scores)
- Raid Boss battles (turn-based combat, team selection, damage formulas)
- Daily missions + weekly goals + pity system
- Progressive set unlock (12 sets gated)
- i18n engine (6 languages, 250+ UI strings, per-card translations)
- Sui wallet integration + on-chain minting + Treasury payment
- Survival profile (Sovereignty vs Dependency analysis)
- Pack history, leaderboards, statistics
- CSS-generated card art with emoji fallback + DALL-E PNGs
- Web Audio procedural sound effects

## Proposed Structure

```
crypto-cards/
├── packages/
│   ├── shared/           # Existing — CardEngine, Gallery, rarity utils
│   ├── rug-museum/       # Existing — 8 rug pull cards
│   ├── sui-ecosystem/    # Existing — 8 Sui protocol cards
│   └── aicards/          # NEW
│       ├── package.json
│       ├── vite.config.js
│       ├── index.html     # Vite entry point
│       ├── public/
│       │   └── images/cards/  # 292 DALL-E PNGs
│       ├── src/
│       │   ├── main.jsx           # Entry, router
│       │   ├── App.jsx            # Tab navigation, state provider
│       │   ├── data/
│       │   │   ├── cards.js       # 294 card objects
│       │   │   ├── bosses.js      # 12 raid bosses
│       │   │   └── sets.js        # Set definitions + unlock logic
│       │   ├── components/
│       │   │   ├── AICardFace.jsx # Custom card renderer
│       │   │   ├── RaidBattle.jsx # Raid boss combat
│       │   │   ├── Missions.jsx   # Daily/weekly missions
│       │   │   ├── BuyPacks.jsx   # SUI purchase flow
│       │   │   ├── Profile.jsx    # Survival profile
│       │   │   └── Stats.jsx      # Leaderboards
│       │   ├── hooks/
│       │   │   ├── useCollection.js  # localStorage state
│       │   │   ├── useSuiWallet.js   # Wallet Standard
│       │   │   └── useI18n.js        # Translation engine
│       │   ├── audio.js           # Web Audio SFX
│       │   └── styles.css         # Extracted CSS
│       ├── lang/                  # i18n JSON files (6 languages)
│       └── contracts/             # Sui Move contracts (symlink or copy)
├── server/                        # Minting API stays at monorepo root (or stays in aicards/)
└── pnpm-workspace.yaml
```

## Migration Phases

### Phase 1: Data Extraction (1 session)
- Extract CARDS array into `data/cards.js`
- Extract raid bosses into `data/bosses.js`
- Extract CSS into `styles.css`
- Verify card counts match

### Phase 2: Core Components (2-3 sessions)
- Create `AICardFace.jsx` (card renderer matching current CSS art)
- Wire up `@crypto-cards/shared` CardEngine for pack opening
- Implement `useCollection` hook (localStorage state, same keys)
- Implement `useI18n` hook (same `t()` / `cardT()` interface)
- Tab navigation (Pull, Collection, Missions, Raid, Profile)

### Phase 3: Game Systems (2-3 sessions)
- Raid Boss battles with team selection + combat
- Daily missions + weekly goals + pity system
- Progressive set unlock
- Survival profile
- Statistics + leaderboards

### Phase 4: Blockchain (1-2 sessions)
- Port `useSuiWallet` hook (Wallet Standard + paste fallback)
- Buy packs with SUI (Treasury payment)
- Auto-mint after pack open
- SuiScan links

### Phase 5: Polish (1 session)
- Web Audio sound effects
- Vercel deployment config
- URL redirect from aicards.fun
- Smoke test all features

## Risks & Decisions

1. **Build step added** — Current architecture is intentionally no-build. Migration adds Vite. Trade-off: enables code reuse, tree-shaking, hot reload. Costs: more complex deploy.

2. **State migration** — Must read existing `aicards2_state` localStorage. New app must be backwards-compatible with existing user collections.

3. **SEO/OG** — Current app works without JS for OG tags. React SPA needs prerendering or meta tags in index.html.

4. **i18n** — Shared engine has no i18n. aicards needs it. Either extend shared or keep it local.

5. **Server** — Minting API stays as-is. No migration needed for server/.

## Recommendation

**Don't rush this.** The single-file app works, is live, and has no performance issues. Migration is a quality-of-life improvement for future card game variants, not a business requirement. Prioritize shipping new sets and marketing over migration.

If migrating: Phase 1 first (data extraction) — this is reversible and proves the concept. If Phase 1 goes clean, continue to Phase 2.
