# CLAUDE.md — aicards-tcg

## Project Overview

AI CARDS — 2030 Survival Edition. A single-file collectible card experience about AI displacement and the humans who survive automation. Gacha-style pack opening with 49 cards across 5 rarities. Live at **aicards.fun**.

## Current State

- **Stack**: Single HTML file (CSS + vanilla JS), no build step
- **Hosting**: Vercel (auto-deploy from GitHub main branch)
- **Domain**: aicards.fun (Vercel DNS)
- **Cards**: 49 total — 10 Legendary, 11 Rare, 11 Uncommon, 8 Common, 9 Junk
- **Series**: S1 (original 37) + S2 (12 new)

## Architecture

```
aicards-tcg/
├── index.html      # The entire app — CSS, JS, card data, all inline
├── og-image.html   # Source file for OG social preview image
├── og-image.png    # Generated 1200x630 social preview
├── CLAUDE.md       # This file
└── .gitignore
```

## Common Commands

```bash
# Deploy (auto on push, or manual)
vercel --prod

# Validate JS syntax
node -e "const h=require('fs').readFileSync('index.html','utf8');const s=h.match(/<script>([\s\S]*?)<\/script>/);new Function(s[1]);console.log('OK')"

# Count cards
grep -c 'rarity:"' index.html

# Screenshot OG image
google-chrome --headless --disable-gpu --screenshot=og-image.png --window-size=1200,630 --hide-scrollbars "file://$(pwd)/og-image.html"

# Run anchormd audit
anchormd audit CLAUDE.md
```

## Domain Context

This is a social commentary piece disguised as a card game. The tone is dark humor — laugh then cry. Cards represent real roles affected by AI automation. The "Karpathy Score" (0-10) measures AI displacement risk. Flavor text should be short, punchy, and hit like a gut punch.

**Card rarities map to survival odds:**
- Legendary (gold) — Trades that cannot be automated (plumber, welder, etc.)
- Rare (purple) — Human purpose roles that resist automation (therapist, nurse, etc.)
- Uncommon (blue) — Society roles being displaced (journalist, accountant, etc.)
- Common (pink) — AI products replacing human connection (AI girlfriend, dating algo, etc.)
- Junk (gray) — Lore characters and meta-commentary (VC, LinkedIn guru, etc.)

## Dependencies

- **Google Fonts**: Cinzel, Cinzel Decorative, IM Fell English, Share Tech Mono
- **html2canvas**: v1.4.1 CDN — card screenshot/share feature
- **Vercel Analytics**: `/_vercel/insights/script.js` + speed insights
- **Web Audio API**: Procedural sound effects (no external audio files)

## Coding Standards

- **Single file**: All CSS, JS, and HTML live in index.html. No build step. Keep it that way.
- **Naming**: camelCase for JS, kebab-case for CSS classes, kebab-case for card IDs
- **Card data**: Each card is a JS object in the CARDS array. Follow existing format exactly.
- **CSS art**: Each card gets an `.art-{id}` class with `::before` (background pattern) and `::after` (emoji icon)
- **Rarity colors**: Use CSS variables (--gold, --purple, --blue, --pink, --gray)
- **State**: localStorage key `aicards2_state`, collection stored as `{cardId: count}` object

## Anti-Patterns (Do NOT Do)

- Do NOT split into multiple files — the single-file architecture is intentional
- Do NOT add a build step, bundler, or framework
- Do NOT use external image assets — all art is CSS-only with emoji overlays
- Do NOT make the tone preachy or moralistic — it should make you laugh, then make you sad
- Do NOT add long flavor text — 2-3 sentences max, every word earns its place
- Do NOT hardcode card counts in HTML — derive from CARDS.length in JS

## Git Conventions

- Commit messages: Conventional commits (`feat:`, `fix:`, `chore:`)
- Push to main triggers Vercel auto-deploy
- Validate JS syntax before committing
