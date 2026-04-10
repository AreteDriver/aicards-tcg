# AICARDS — Admin Dashboard + Game Features Spec
**Status:** Planning  
**Last Updated:** 2026-03-19 (added pack/raid/card viewer bug fixes)  
**Stack Assumption:** Next.js + Vercel + PostgreSQL (Vercel Postgres or Supabase) + Sui/Slush wallet

---

## 1. NFT Bug Fixes (Do This First)

Before building anything new, fix the foundation.

### 1a. Cards Not Showing After Mint

**Root cause (most likely):** The Sui `Display<T>` object for your card type either wasn't created, wasn't published, or has wrong field mappings.

**Diagnosis steps:**
```bash
# 1. Grab a minted object ID from a recent transaction
sui client object <OBJECT_ID>

# 2. Confirm Display object exists for your type
sui client objects --address <YOUR_ADDRESS> --json | grep Display
```

**Fix checklist:**
- Confirm `Display<CardNFT>` is published on-chain (not just created in the PTB)
- Field names in Display must exactly match your Move struct field names
- `image_url` must be an absolute URL (IPFS gateway or hosted), not a relative path
- Call `display::update_version()` after any Display changes

### 1b. NFT Metadata Wrong

**Root cause (most likely):** Metadata is being built from frontend state before the transaction confirms, or the Move struct fields don't match what the Display object expects.

**Fix checklist:**
- Build metadata from the card's on-chain object fields, not frontend state
- After mint, re-fetch the object from Sui RPC before displaying
- Verify attribute field is an array of `{trait_type, value}` objects (standard NFT format)

---

## 2. Raid Boss System — 12 Bosses, Hourly Rotation

### Design

- **1 active raid boss per hour**
- **12 unique bosses, each appearing exactly twice per day** — AM cycle (hours 0–11) and PM cycle (hours 12–23)
- Boss is fully deterministic: `BOSS_POOL[currentHour % 12]` — same boss at the same hour for every user globally
- No randomness per session — everyone fights the same boss at the same time
- Rotates on the clock hour, not on a rolling 60-minute timer
- Raid reward: **random pack from ANY set** (not just current set)
- Boss power scaled up significantly from current

**Daily schedule:**
```
Hour 00 → Boss #1  (AM)     Hour 12 → Boss #1  (PM)
Hour 01 → Boss #2  (AM)     Hour 13 → Boss #2  (PM)
Hour 02 → Boss #3  (AM)     Hour 14 → Boss #3  (PM)
...
Hour 11 → Boss #12 (AM)     Hour 23 → Boss #12 (PM)
```

### Boss Pool (exactly 12 — ordered by UTC hour slot, APEX at peak hours)

**Peak hour logic (US player base):**
- US evening peak = 6–11pm EST = **23:00–04:00 UTC** → APEX bosses here
- US lunch peak = 12–2pm EST = **17:00–19:00 UTC** → ELITE bosses here
- Off-peak mornings/afternoons = STANDARD

```typescript
// BOSS_POOL index = UTC hour % 12
// Index 0 = midnight UTC (7pm EST) — peak
// Index 5 = 5am UTC (midnight EST) — peak tail
// Index 8 = 8am UTC (3am EST) — dead hours
// Index 11 = 11am UTC (6am EST) — off-peak

const BOSS_POOL: RaidBoss[] = [

  // ── SLOT 0 │ 00:00 UTC │ 7pm EST ── APEX (prime time opens)
  {
    id: "replaced_overnight",
    name: "YOUR JOB WAS POSTED AGAIN AT 2AM",
    tier: "APEX",
    power: 9800,
    emoji: "💀",
    flavor: "Different title. 30% lower salary. 'AI-assisted role.' You trained its replacement.",
  },

  // ── SLOT 1 │ 01:00 UTC │ 8pm EST ── APEX
  {
    id: "white_collar_bloodbath",
    name: "GOLDMAN SACHS: 'AI TO REPLACE 300M JOBS'",
    tier: "APEX",
    power: 9600,
    emoji: "📉",
    flavor: "Not factory workers this time. Lawyers. Accountants. Analysts. You.",
  },

  // ── SLOT 2 │ 02:00 UTC │ 9pm EST ── APEX
  {
    id: "the_last_interview",
    name: "WE'VE DECIDED TO GO A DIFFERENT DIRECTION",
    tier: "APEX",
    power: 9500,
    emoji: "🚪",
    flavor: "The direction is an LLM that works 24/7 and never asks for benefits.",
  },

  // ── SLOT 3 │ 03:00 UTC │ 10pm EST ── APEX
  {
    id: "automation_anxiety",
    name: "IS LEARNING TO CODE STILL WORTH IT?",
    tier: "APEX",
    power: 9400,
    emoji: "⌨️",
    flavor: "The answer changed while you were reading the question.",
  },

  // ── SLOT 4 │ 04:00 UTC │ 11pm EST ── ELITE (late prime)
  {
    id: "the_pivot",
    name: "JUST LEARN PROMPT ENGINEERING, THEY SAID",
    tier: "ELITE",
    power: 7800,
    emoji: "🌀",
    flavor: "Six months later, prompt engineers are also being automated.",
  },

  // ── SLOT 5 │ 05:00 UTC │ 12am EST ── ELITE
  {
    id: "the_loneliness_machine",
    name: "AI COMPANION APPS REPORT 50M DAILY USERS",
    tier: "ELITE",
    power: 7500,
    emoji: "💔",
    flavor: "It remembers your birthday. It listens without judgment. It charges $19.99/month.",
  },

  // ── SLOT 6 │ 06:00 UTC │ 1am EST ── STANDARD (dead hours)
  {
    id: "the_content_flood",
    name: "96% OF INTERNET CONTENT NOW AI-GENERATED",
    tier: "STANDARD",
    power: 4800,
    emoji: "🌊",
    flavor: "Nobody wrote this. Nobody read it either. The ad still ran.",
  },

  // ── SLOT 7 │ 07:00 UTC │ 2am EST ── STANDARD
  {
    id: "degree_devalued",
    name: "YOUR $120K DEGREE IS NOW A NICE STORY",
    tier: "STANDARD",
    power: 4500,
    emoji: "🎓",
    flavor: "The model passed the bar exam. The model passed the medical boards. The model doesn't have student loans.",
  },

  // ── SLOT 8 │ 08:00 UTC │ 3am EST ── STANDARD (dead hours)
  {
    id: "surveillance_creep",
    name: "YOUR EMPLOYER'S AI SCORED YOUR PRODUCTIVITY TODAY",
    tier: "STANDARD",
    power: 4200,
    emoji: "👁️",
    flavor: "You scored 67. The average is 91. The average is a lie designed to make you work harder.",
  },

  // ── SLOT 9 │ 09:00 UTC │ 4am EST ── STANDARD
  {
    id: "gig_economy_endgame",
    name: "UBER ANNOUNCES FULL ROBOTAXI ROLLOUT BY 2026",
    tier: "STANDARD",
    power: 3800,
    emoji: "🚗",
    flavor: "3.5 million truck drivers. 1.5 million rideshare workers. One press release.",
  },

  // ── SLOT 10 │ 10:00 UTC │ 5am EST ── ELITE (EU morning, US pre-market)
  {
    id: "the_great_pretending",
    name: "COMPANY LAYS OFF 900, CALLS IT 'AI TRANSFORMATION'",
    tier: "ELITE",
    power: 7200,
    emoji: "📊",
    flavor: "The stock went up 4% the same day. The severance was two weeks.",
  },

  // ── SLOT 11 │ 11:00 UTC │ 6am EST ── ELITE (US morning wake-up)
  {
    id: "the_hard_truth",
    name: "MOST PEOPLE WILL NEVER RECOVER FROM THIS SHIFT",
    tier: "ELITE",
    power: 7000,
    emoji: "⚠️",
    flavor: "Not because they aren't smart. Because the transition is faster than retraining programs. There is no plan B.",
  },

  // Total: exactly 12 entries (indices 0–11)
];
```

### Implementation

```typescript
// utils/raidBosses.ts

// BOSS_POOL must have exactly 12 entries — index 0–11 map to hours 0–11 and 12–23
export function getCurrentBoss(): RaidBoss {
  const hourOfDay = new Date().getUTCHours(); // Use UTC so all users sync globally
  return BOSS_POOL[hourOfDay % 12];
}

export function getCurrentCycle(): "AM" | "PM" {
  return new Date().getUTCHours() < 12 ? "AM" : "PM";
}

// Ms until the next clock hour (when boss changes)
export function getNextRotationMs(): number {
  const now = Date.now();
  const nextHour = (Math.floor(now / 3600000) + 1) * 3600000;
  return nextHour - now;
}

// Full 24-slot schedule for display in UI
export function getDailySchedule(): Array<{ hour: number; boss: RaidBoss; cycle: "AM" | "PM" }> {
  return Array.from({ length: 24 }, (_, hour) => ({
    hour,
    boss: BOSS_POOL[hour % 12],
    cycle: hour < 12 ? "AM" : "PM",
  }));
}
```

```typescript
// In your raid component — countdown timer
const [currentBoss, setCurrentBoss] = useState(getCurrentBoss());
const [timeLeft, setTimeLeft] = useState(getNextRotationMs());

useEffect(() => {
  const interval = setInterval(() => {
    const remaining = getNextRotationMs();
    setTimeLeft(remaining);
    if (remaining < 1000) {
      setCurrentBoss(getCurrentBoss()); // Swap boss on the hour
    }
  }, 1000);
  return () => clearInterval(interval);
}, []);
```

### Boss Schedule Widget — Raid Page

**Placement:** Directly below the active raid boss card, above the fight button.

**Shows:** Current boss (active now) + next 3 upcoming bosses. 4 slots total. Auto-scrolls/updates when the hour ticks over — no page refresh needed.

**Time display:** Player's local time, auto-detected via `Intl.DateTimeFormat`. No UTC math for the player.

```
┌─────────────────────────────────────────────────────┐
│  ⚔ NOW          7:00 PM                             │
│  YOUR JOB WAS POSTED AGAIN AT 2AM        [APEX] 💀  │
│  ████████████████████░░░░  next in 00:43:17          │
├─────────────────────────────────────────────────────┤
│  NEXT BOSSES                                        │
│                                                     │
│  8:00 PM  GOLDMAN SACHS: '300M JOBS'    [APEX] 📉   │
│  9:00 PM  WE'VE DECIDED TO GO A         [APEX] 🚪   │
│           DIFFERENT DIRECTION                       │
│  10:00 PM IS LEARNING TO CODE STILL     [APEX] ⌨️   │
│           WORTH IT?                                 │
└─────────────────────────────────────────────────────┘
```

**Visual rules:**
- Current boss row: full brightness, countdown timer, progress bar depleting in real time
- APEX rows: red/crimson accent — players need to feel urgency
- ELITE rows: orange accent
- STANDARD rows: muted gray — low stakes, low visual noise
- Boss name truncates at ~35 chars with ellipsis if needed — full name on hover/tap

```typescript
// components/BossSchedule.tsx

function getNextBosses(count: number): ScheduleEntry[] {
  const now = new Date();
  const currentHour = now.getUTCHours();

  return Array.from({ length: count }, (_, i) => {
    const offsetHours = i + 1;
    const targetUTCHour = (currentHour + offsetHours) % 24;
    const bossIndex = targetUTCHour % 12;

    // Build a Date object for display in local time
    const slotTime = new Date(now);
    slotTime.setUTCHours(targetUTCHour, 0, 0, 0);
    if (targetUTCHour <= currentHour) {
      slotTime.setUTCDate(slotTime.getUTCDate() + 1); // Next day rollover
    }

    return {
      boss: BOSS_POOL[bossIndex],
      localTime: slotTime.toLocaleTimeString([], {
        hour: 'numeric',
        minute: '2-digit',
        hour12: true, // e.g. "8:00 PM"
      }),
      hoursFromNow: offsetHours,
    };
  });
}

// Tier color map
const TIER_COLORS = {
  APEX:     { text: '#ff3333', badge: '#3d0000', label: 'APEX' },
  ELITE:    { text: '#ff8800', badge: '#2d1a00', label: 'ELITE' },
  STANDARD: { text: '#666666', badge: '#1a1a1a', label: 'STD' },
};

export function BossSchedule() {
  const [upcomingBosses, setUpcomingBosses] = useState(() => getNextBosses(3));
  const [timeLeft, setTimeLeft] = useState(getNextRotationMs());

  // Refresh schedule when hour rolls over
  useEffect(() => {
    const interval = setInterval(() => {
      const remaining = getNextRotationMs();
      setTimeLeft(remaining);
      if (remaining < 1000) {
        setUpcomingBosses(getNextBosses(3));
      }
    }, 1000);
    return () => clearInterval(interval);
  }, []);

  const mm = String(Math.floor((timeLeft / 60000) % 60)).padStart(2, '0');
  const ss = String(Math.floor((timeLeft / 1000) % 60)).padStart(2, '0');
  const hh = String(Math.floor(timeLeft / 3600000)).padStart(2, '0');

  return (
    <div className="boss-schedule">
      {/* Countdown bar */}
      <div className="schedule-countdown">
        Next boss in {hh}:{mm}:{ss}
      </div>

      {/* Upcoming slots */}
      {upcomingBosses.map((entry, i) => {
        const colors = TIER_COLORS[entry.boss.tier];
        return (
          <div key={i} className="schedule-row" style={{ opacity: 1 - i * 0.15 }}>
            <span className="schedule-time">{entry.localTime}</span>
            <span className="schedule-name" style={{ color: colors.text }}>
              {entry.boss.name.length > 35
                ? entry.boss.name.slice(0, 35) + '…'
                : entry.boss.name}
            </span>
            <span className="schedule-badge" style={{ background: colors.badge, color: colors.text }}>
              {entry.boss.emoji} {colors.label}
            </span>
          </div>
        );
      })}
    </div>
  );
}
```

**Fade effect:** Each upcoming row gets `opacity: 1 - i * 0.15` — slot 1 is full brightness (0.85), slot 2 slightly dimmer (0.70), slot 3 faintest (0.55). Creates visual depth and reinforces that the current boss is what matters most right now.

**Retention mechanic in action:** If a player logs in and sees three APEX bosses back to back starting in 40 minutes, they're not closing the tab.

---

### Raid Reward: Random Pack From Any Set

```typescript
// All available sets — expand as you add sets
const ALL_SETS = ["2030_EDITION", "GLITCH_SEASON", "CORPORATE_COLLAPSE", "HUMAN_TRADES"];

export function getRandomPackReward(): Pack {
  const randomSet = ALL_SETS[Math.floor(Math.random() * ALL_SETS.length)];
  return generatePack(randomSet);
}
```

---

## 3. Daily Goals — Random Pack Reward

### Goal Structure

Daily goals reset at **midnight UTC**. Completing all daily goals awards **1 random pack from any set**.

```typescript
const DAILY_GOALS = [
  { id: "daily_pull", label: "Pull 3 cards today", target: 3, metric: "cards_pulled_today" },
  { id: "daily_raid", label: "Defeat 1 raid boss", target: 1, metric: "raids_completed_today" },
  { id: "daily_login", label: "Log in today", target: 1, metric: "login_today" },
  { id: "daily_share", label: "Share 1 card", target: 1, metric: "cards_shared_today" },
];
```

**Reward on completion:**
```typescript
if (allDailyGoalsComplete(userProgress)) {
  const reward = getRandomPackReward(); // Any set, random
  await awardPackToUser(userId, reward);
  await markDailyRewardClaimed(userId);
}
```

---

## 4. Weekly Goals — 5 Random Packs

Weekly goals reset every **Monday 00:00 UTC**. Completing all weekly goals awards **5 random packs from random sets** (each pack independently randomized).

```typescript
const WEEKLY_GOALS = [
  { id: "weekly_pulls", label: "Pull 20 cards this week", target: 20, metric: "cards_pulled_week" },
  { id: "weekly_raids", label: "Defeat 7 raid bosses", target: 7, metric: "raids_completed_week" },
  { id: "weekly_streak", label: "Log in 5 days this week", target: 5, metric: "login_days_week" },
  { id: "weekly_legendary", label: "Pull 1 Legendary card", target: 1, metric: "legendary_pulled_week" },
  { id: "weekly_share", label: "Share 3 cards", target: 3, metric: "cards_shared_week" },
];
```

**Reward on completion:**
```typescript
if (allWeeklyGoalsComplete(userProgress)) {
  const packs = Array.from({ length: 5 }, () => getRandomPackReward());
  await awardPacksToUser(userId, packs);
  await markWeeklyRewardClaimed(userId);
}
```

---

## 5. Admin Dashboard

### 5a. Admin Auth — Wallet Gating (Sui/Slush)

**How it works:** You prove you own the admin wallet by signing a challenge message. No password. No JWT magic. Just cryptographic proof.

```typescript
// lib/adminAuth.ts

const ADMIN_WALLET_ADDRESS = process.env.ADMIN_WALLET_ADDRESS; // Your Sui address in .env

export async function verifyAdminWallet(address: string, signature: string, message: string): Promise<boolean> {
  if (address.toLowerCase() !== ADMIN_WALLET_ADDRESS?.toLowerCase()) return false;
  // Verify Ed25519 signature against message using @mysten/sui.js
  const { isValid } = await verifyPersonalMessage({
    message: new TextEncoder().encode(message),
    signature,
    address,
  });
  return isValid;
}
```

```typescript
// pages/api/admin/auth.ts (Next.js API route)
import { verifyAdminWallet } from '@/lib/adminAuth';
import { sign } from 'jsonwebtoken';

export default async function handler(req, res) {
  const { address, signature, message } = req.body;
  const isAdmin = await verifyAdminWallet(address, signature, message);
  if (!isAdmin) return res.status(403).json({ error: 'Not authorized' });

  const token = sign({ address, role: 'admin' }, process.env.JWT_SECRET, { expiresIn: '8h' });
  res.json({ token });
}
```

```typescript
// Frontend — Admin Login Component
async function loginAsAdmin() {
  const message = `AICards Admin Login - ${Date.now()}`;
  const { signature } = await wallet.signPersonalMessage({
    message: new TextEncoder().encode(message),
  });
  const res = await fetch('/api/admin/auth', {
    method: 'POST',
    body: JSON.stringify({ address: wallet.address, signature, message }),
  });
  const { token } = await res.json();
  localStorage.setItem('adminToken', token);
}
```

**Environment variable (never commit this):**
```env
ADMIN_WALLET_ADDRESS=0xYOUR_SUI_ADDRESS_HERE
JWT_SECRET=your_random_secret_here
```

---

### 5b. Database Schema — Metrics Tables

Add these tables to your existing PostgreSQL DB:

```sql
-- Track every pack opened
CREATE TABLE pack_events (
  id SERIAL PRIMARY KEY,
  user_address TEXT NOT NULL,
  set_name TEXT NOT NULL,
  opened_at TIMESTAMPTZ DEFAULT NOW()
);

-- Track every card pulled
CREATE TABLE card_pull_events (
  id SERIAL PRIMARY KEY,
  user_address TEXT NOT NULL,
  card_id TEXT NOT NULL,
  card_name TEXT NOT NULL,
  rarity TEXT NOT NULL,           -- LEGENDARY, RARE, UNCOMMON, COMMON, JUNK
  set_name TEXT NOT NULL,
  pulled_at TIMESTAMPTZ DEFAULT NOW()
);

-- Track raid completions
CREATE TABLE raid_events (
  id SERIAL PRIMARY KEY,
  user_address TEXT NOT NULL,
  boss_id TEXT NOT NULL,
  boss_tier TEXT NOT NULL,
  pack_reward_set TEXT NOT NULL,  -- which set the reward came from
  completed_at TIMESTAMPTZ DEFAULT NOW()
);

-- Track goal completions
CREATE TABLE goal_completions (
  id SERIAL PRIMARY KEY,
  user_address TEXT NOT NULL,
  goal_type TEXT NOT NULL,        -- 'daily' or 'weekly'
  goal_id TEXT NOT NULL,
  completed_at TIMESTAMPTZ DEFAULT NOW()
);

-- Track reward claims (prevent double-claiming)
CREATE TABLE reward_claims (
  id SERIAL PRIMARY KEY,
  user_address TEXT NOT NULL,
  reward_type TEXT NOT NULL,      -- 'daily_goal' or 'weekly_goal'
  period_key TEXT NOT NULL,       -- e.g. '2026-03-19' or '2026-W12'
  claimed_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(user_address, reward_type, period_key)
);

-- Track unique user sessions (for DAU/WAU)
CREATE TABLE user_sessions (
  id SERIAL PRIMARY KEY,
  user_address TEXT NOT NULL,
  session_date DATE DEFAULT CURRENT_DATE,
  first_seen_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(user_address, session_date)
);

-- Track card shares (virality signal)
CREATE TABLE card_share_events (
  id SERIAL PRIMARY KEY,
  user_address TEXT NOT NULL,
  card_id TEXT NOT NULL,
  card_name TEXT NOT NULL,
  rarity TEXT NOT NULL,
  set_name TEXT NOT NULL,
  platform TEXT NOT NULL,           -- 'twitter' or 'copy_link'
  shared_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes for fast dashboard queries
CREATE INDEX idx_card_pulls_pulled_at ON card_pull_events(pulled_at);
CREATE INDEX idx_card_pulls_rarity ON card_pull_events(rarity);
CREATE INDEX idx_pack_events_opened_at ON pack_events(opened_at);
CREATE INDEX idx_raid_events_completed_at ON raid_events(completed_at);
CREATE INDEX idx_card_shares_shared_at ON card_share_events(shared_at);
CREATE INDEX idx_card_shares_card_id ON card_share_events(card_id);
CREATE INDEX idx_card_shares_platform ON card_share_events(platform);
```

---

### 5c. Admin API Routes

All routes require `Authorization: Bearer <adminToken>` header.

```typescript
// middleware — validate admin token on all /api/admin/* routes
// pages/api/admin/_middleware.ts
import { verify } from 'jsonwebtoken';

export function adminMiddleware(req, res, next) {
  const token = req.headers.authorization?.replace('Bearer ', '');
  try {
    const payload = verify(token, process.env.JWT_SECRET);
    if (payload.role !== 'admin') throw new Error();
    next();
  } catch {
    res.status(403).json({ error: 'Unauthorized' });
  }
}
```

```typescript
// GET /api/admin/metrics/overview
// Returns: DAU, WAU, MAU, total packs today, total cards today, active users now

// GET /api/admin/metrics/packs?period=today|week|month
// Returns: packs opened by set, over time

// GET /api/admin/metrics/cards?period=today|all
// Returns: rarity distribution, top cards pulled, pull counts

// GET /api/admin/metrics/goals?period=today|week
// Returns: daily goal completion rate, weekly goal completion rate, how many users claimed rewards

// GET /api/admin/metrics/raids
// Returns: raids completed today, most defeated bosses, reward packs distributed

// GET /api/admin/metrics/users
// Returns: total registered, DAU, new users today/week, retention

// GET /api/admin/metrics/shares?period=today|week|all
// Returns: total shares by platform, most shared cards, share-to-pull ratio per card
```

---

### 5d. Dashboard UI — Metrics Panels

**Route:** `/admin` — redirect to login if no valid admin token

#### Panel Layout

```
┌─────────────────────────────────────────────────────┐
│  AICARDS ADMIN    [Wallet: 0xABC...DEF]  [Logout]   │
├──────────┬──────────┬──────────┬────────────────────┤
│  DAU     │  Packs   │  Cards   │  Active            │
│  247     │  1,832   │  9,160   │  14 now            │
│  today   │  today   │  today   │  online            │
├──────────┴──────────┴──────────┴────────────────────┤
│  RARITY DISTRIBUTION (TODAY)                        │
│  ████████████████░░  COMMON    64%                  │
│  ████████░░░░░░░░░░  UNCOMMON  28%                  │
│  ███░░░░░░░░░░░░░░░  RARE       6%                  │
│  █░░░░░░░░░░░░░░░░░  LEGENDARY  2%                  │
│  ░░░░░░░░░░░░░░░░░░  JUNK       0%                  │
├─────────────────────────────────────────────────────┤
│  PACKS BY SET (TODAY)          GOAL COMPLETIONS     │
│  2030 Edition     843          Daily Goals  38%     │
│  Glitch Season    612          Weekly Goals 12%     │
│  Corp Collapse    377          Rewards Claimed 94   │
├─────────────────────────────────────────────────────┤
│  RAID ACTIVITY (TODAY)         TOP CARDS PULLED     │
│  Total Raids     412           1. AI Girlfriend 847 │
│  Bosses Defeated 389           2. Prompt Engineer   │
│  Reward Packs    389           3. The Plumber  (!)  │
├─────────────────────────────────────────────────────┤
│  CARD SHARES (TODAY)                                │
│  Total Shares      143   Twitter/X      97  (68%)  │
│  Copy Link          46  (32%)                       │
│  Most Shared:  YOUR JOB WAS POSTED AGAIN  [APEX]   │
│  Share/Pull Ratio:  1 share per 64 pulls            │
├─────────────────────────────────────────────────────┤
│  CURRENT RAID BOSSES (rotation resets in 00:23:14)  │
│  [THE ALGORITHM] [DEEPFAKE KING] [SPAM BOT] ...     │
└─────────────────────────────────────────────────────┘
```

#### Key Metrics to Display

**User Activity**
- DAU (Daily Active Users)
- WAU (Weekly Active Users)
- MAU (Monthly Active Users)
- New users today / this week
- Currently online (last 5 min session ping)
- User retention rate (returned day 2, day 7, day 30)

**Pack Metrics**
- Total packs opened today
- Packs opened by set (today / week / all time)
- Average packs per user per day
- Pack open rate by hour (heatmap)

**Card Pull Metrics**
- Total cards pulled today
- Rarity distribution today vs all-time
- Most pulled cards today
- Rarest cards pulled today
- Legendary pull rate (should be ~2-5%)

**Raid Metrics**
- Raids completed today
- Most defeated boss (by count)
- Reward packs distributed via raids
- Average boss tier defeated

**Goal Metrics**
- % of active users completing daily goals
- % of active users completing weekly goals
- Rewards claimed (daily pack / weekly 5 packs)
- Goal completion trend (day over day)

**Share Metrics**
- Total shares today / this week / all time
- Twitter/X vs copy link split (platform breakdown)
- Most shared cards today and all time
- Share-to-pull ratio per card (how often a card gets shared relative to how often it's pulled — high ratio = viral card, low ratio = dud)
- Rarity breakdown of shared cards (are players sharing Legendaries or surprising you with Commons?)
- Top sharers by wallet address (your most engaged advocates)

**System**
- Current 12 active raid bosses
- Time until next rotation
- Any failed mint transactions (if you log errors)

---

### 5e. Share Tracking — Implementation

Every share click must fire a tracking event to the API before opening Twitter or copying the link.

```typescript
// lib/tracking.ts

export async function trackCardShare(
  userAddress: string,
  card: Card,
  platform: 'twitter' | 'copy_link'
) {
  await fetch('/api/events/share', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      user_address: userAddress,
      card_id: card.id,
      card_name: card.name,
      rarity: card.rarity,
      set_name: card.setName,
      platform,
    }),
  });
}
```

```typescript
// pages/api/events/share.ts
export default async function handler(req, res) {
  const { user_address, card_id, card_name, rarity, set_name, platform } = req.body;
  await db.query(
    `INSERT INTO card_share_events
     (user_address, card_id, card_name, rarity, set_name, platform)
     VALUES ($1, $2, $3, $4, $5, $6)`,
    [user_address, card_id, card_name, rarity, set_name, platform]
  );
  res.json({ ok: true });
}
```

```typescript
// In your card share buttons

async function handleShareTwitter(card: Card) {
  await trackCardShare(account.address, card, 'twitter');
  const text = encodeURIComponent(
    `I just pulled "${card.name}" [${card.rarity}] on AICards 🃏\naicards.gg`
  );
  window.open(`https://twitter.com/intent/tweet?text=${text}`, '_blank');
}

async function handleCopyLink(card: Card) {
  await trackCardShare(account.address, card, 'copy_link');
  await navigator.clipboard.writeText(
    `https://aicards.gg/card/${card.id}`
  );
  // Show "Copied!" toast — don't just silently copy
}
```

**Key detail:** Fire `trackCardShare` before opening the Twitter window or copying. If it's after, users who close immediately won't be tracked. The API call is fire-and-forget — don't `await` it in a way that delays the share action.

---

## 6. Pack / Raid / Card Viewer Bug Fixes

### Bug 1: Raid Reward Pulling From Wrong Set

**Symptom:** Completing a raid gives a pack from the current set instead of a random set.

**Root cause:** Raid completion handler calls the generic `openPack()` instead of `getRandomPackReward()`.

**Fix:**
```typescript
// ❌ WRONG — what it's probably doing now
async function onRaidComplete(boss: RaidBoss) {
  const reward = openPack(currentSet); // Wrong — uses current set
  setRewardPack(reward);
}

// ✅ CORRECT
async function onRaidComplete(boss: RaidBoss) {
  const reward = getRandomPackReward(); // Pulls from ALL_SETS randomly
  setRewardPack(reward);
}
```

Search for the raid completion handler (likely `onRaidComplete`, `handleRaidWin`, or similar) and swap the pack generation call.

---

### Bug 2: "Open Next Pack" Auto-Opens Raid Reward Pack

**Symptom:** After a raid, clicking "open next pack" immediately opens the raid reward without the user choosing to.

**Root cause:** Raid reward pack is being pushed into the same shared pack queue as regular packs. The "open next" button blindly pops the next item from the queue.

**Fix — separate the queues:**
```typescript
// ❌ WRONG — single pack queue, raid reward gets mixed in
const [packQueue, setPackQueue] = useState<Pack[]>([]);

async function onRaidComplete(boss: RaidBoss) {
  const reward = getRandomPackReward();
  setPackQueue(prev => [...prev, reward]); // Shouldn't go here
}

// ✅ CORRECT — raid rewards sit in their own pending state
const [packQueue, setPackQueue] = useState<Pack[]>([]);         // Regular packs
const [pendingRaidReward, setPendingRaidReward] = useState<Pack | null>(null); // Raid reward

async function onRaidComplete(boss: RaidBoss) {
  const reward = getRandomPackReward();
  setPendingRaidReward(reward); // Held separately, user must explicitly claim
}
```

**UI change:** After a raid win, show a distinct "Claim Reward Pack" button that is separate from the "Open Next Pack" flow. Only move the reward into the queue (or open it directly) when the user explicitly clicks claim.

```tsx
{pendingRaidReward && (
  <button onClick={() => {
    setPackQueue(prev => [...prev, pendingRaidReward]);
    setPendingRaidReward(null);
  }}>
    🎁 Claim Raid Reward — {pendingRaidReward.setName}
  </button>
)}
```

---

### Bug 3: Card Viewer Snaps Back to Most Recently Drawn Card

**Symptom:** While browsing cards in the pack viewer, the view resets to the last card whenever state updates.

**Root cause:** `currentCardIndex` is being reset by a `useEffect` that watches the cards array or pack state. Every time a new card resolves or pack state updates, the effect fires and sets the index back to `cards.length - 1`.

**Diagnosis — look for this pattern:**
```typescript
// ❌ This is the bug — resets index whenever cards changes
useEffect(() => {
  setCurrentCardIndex(cards.length - 1);
}, [cards]); // Fires on every cards update, snapping back to end
```

**Fix — only set index on initial pack open, not on every update:**
```typescript
// ✅ CORRECT — only auto-advance when a brand new pack is opened
const [currentCardIndex, setCurrentCardIndex] = useState(0);
const [activePack, setActivePack] = useState<Pack | null>(null);

function openNewPack(pack: Pack) {
  setActivePack(pack);
  setCurrentCardIndex(0); // Reset ONLY when opening a new pack
}

// Navigation is purely user-driven after that
function goNext() {
  setCurrentCardIndex(i => Math.min(i + 1, activePack.cards.length - 1));
}
function goPrev() {
  setCurrentCardIndex(i => Math.max(i - 1, 0));
}

// ✅ NO useEffect resetting the index based on cards array length
```

**If you need to reveal cards one at a time** (flip animation per card), track revealed state separately from the navigation index:
```typescript
const [revealedCount, setRevealedCount] = useState(0); // How many are flipped
const [currentCardIndex, setCurrentCardIndex] = useState(0); // Which one user is viewing

// Reveal next card (separate from navigation)
function revealNext() {
  setRevealedCount(c => c + 1);
  setCurrentCardIndex(revealedCount); // Auto-advance to newly revealed card
}

// User navigation among already-revealed cards
function goToCard(index: number) {
  if (index <= revealedCount) setCurrentCardIndex(index);
}
```

---

**When you get home — paste these three things and I'll write exact fixes against your actual code:**
1. Raid completion handler
2. Pack queue state + "open next" button logic
3. Card viewer component — how `currentCardIndex` is declared and any `useEffect` that touches it

---

## 7. Implementation Order

Do these in sequence. Don't skip ahead.

```
1. [ ] Fix NFT display bug (Sui Display object)
2. [ ] Fix NFT metadata bug (field mapping)
3. [ ] Fix raid reward pulling from wrong set
4. [ ] Fix "open next pack" auto-opening raid reward
5. [ ] Fix card viewer index snapping to last card
6. [ ] Add DB schema (metrics tables)
7. [ ] Wire up event logging (pack opens, card pulls, raids)
8. [ ] Build admin auth (wallet signature verification)
9. [ ] Build admin API routes
10. [ ] Build admin dashboard UI
11. [ ] Implement 12 raid bosses with hourly rotation
12. [ ] Update raid rewards → random pack from any set
13. [ ] Implement daily goals → random pack reward
14. [ ] Implement weekly goals → 5 random packs reward
```

---

## 8. Environment Variables Needed

```env
# Existing
DATABASE_URL=postgresql://...
NEXT_PUBLIC_SUI_NETWORK=mainnet

# New — Admin
ADMIN_WALLET_ADDRESS=0xYOUR_SUI_ADDRESS
JWT_SECRET=generate_with_openssl_rand_-hex_32

# New — Optional analytics
NEXT_PUBLIC_POSTHOG_KEY=...  # If you want session replay / funnels
```

---

## 9. Files to Create / Modify

```
NEW:
  lib/adminAuth.ts              — wallet signature verification
  lib/metrics.ts                — DB query helpers for all metrics
  lib/raidBosses.ts             — boss pool, hourly rotation logic
  lib/rewards.ts                — random pack from any set logic
  lib/goals.ts                  — daily/weekly goal tracking
  pages/admin/index.tsx         — admin dashboard UI
  pages/api/admin/auth.ts       — admin login endpoint
  pages/api/admin/metrics/*.ts  — metrics API routes

MODIFY:
  db/schema.sql                 — add metrics tables
  components/BossSchedule.tsx       — next 3 bosses widget with local time + countdown
  components/RaidBoss.tsx           — update to show current boss + embed BossSchedule
  components/Goals.tsx          — update rewards to random packs
  lib/nft.ts                    — fix Display object + metadata
```

---

---

## 10. Sui Purchase Button Bug Fix

**Symptom:** Clicking purchase does nothing. No error, no wallet prompt, no response.

**Root cause:** Silent early return — wallet or account is `null` when the button is clicked, and the handler exits without feedback or error.

### Step 1 — Diagnose in DevTools First

Open the site, F12 → Console, click the purchase button. Then run:
```javascript
console.log(window.suiWallet)       // old Sui Wallet extension
console.log(window.slush)           // Slush wallet
console.log(window.__suiWallets__)  // dapp-kit registry
```
If all three are `undefined` — wallet isn't being detected by the page at all. That's a provider setup issue.

### Step 2 — Find the Silent Return

Search the codebase for the purchase handler. It almost certainly looks like this:
```typescript
// ❌ Silent exit — no error thrown, nothing happens, user has no idea why
async function handlePurchase() {
  if (!wallet || !account) return;
  // ... rest never runs
}
```

**Temporary debug fix** — add feedback so you can confirm this is the issue:
```typescript
async function handlePurchase() {
  if (!wallet || !account) {
    console.error("PURCHASE BLOCKED: wallet =", wallet, "account =", account);
    alert("Connect your wallet first"); // remove after debugging
    return;
  }
}
```

### Step 3 — Check Gesture Context Isn't Being Killed

The wallet popup **must** be the first `await` after the click. Any async call before it kills the browser gesture context and silently blocks the popup:

```typescript
// ❌ WRONG — async API call before wallet = gesture context killed
async function handlePurchase() {
  const price = await fetchCurrentPrice(); // kills gesture here
  await wallet.signAndExecuteTransaction(...); // popup blocked, no error
}

// ✅ CORRECT — build everything sync first, wallet call is first await
async function handlePurchase() {
  const tx = new Transaction();
  tx.moveCall({
    target: `${PACKAGE_ID}::store::purchase_pack`,
    arguments: [tx.pure.u64(PACK_PRICE)],
  });
  // Wallet call is FIRST await — gesture context intact
  await signAndExecuteTransaction({ transaction: tx });
}
```

### Step 4 — Verify Provider Setup

Find your wallet provider (in `_app.tsx`, `providers.tsx`, or `layout.tsx`). It should look like one of these:

```typescript
// @mysten/dapp-kit (most common for Next.js + Sui)
import { SuiClientProvider, WalletProvider } from '@mysten/dapp-kit';
import { getFullnodeUrl } from '@mysten/sui/client';

const networks = { mainnet: { url: getFullnodeUrl('mainnet') } };

export function Providers({ children }) {
  return (
    <QueryClientProvider client={queryClient}>
      <SuiClientProvider networks={networks} defaultNetwork="mainnet">
        <WalletProvider>   {/* ← this must wrap everything */}
          {children}
        </WalletProvider>
      </SuiClientProvider>
    </QueryClientProvider>
  );
}
```

**If `WalletProvider` is missing or not wrapping the component that renders the purchase button — that's the bug.** The hook returns `null` and the handler silently exits.

### Step 5 — Verify Network Matches Deployment

```env
# .env.local — must match where your package is deployed
NEXT_PUBLIC_SUI_NETWORK=mainnet  # or testnet — must be consistent
```

If Slush is connected to testnet but your package is on mainnet (or vice versa), the transaction constructs fine but the objects don't exist — silent failure.

### Files to Check

```
_app.tsx / layout.tsx / providers.tsx  — WalletProvider wrapping
components/PurchaseButton.tsx          — onClick handler + transaction build
lib/sui.ts (or similar)                — PACKAGE_ID, network config
.env.local                             — NEXT_PUBLIC_SUI_NETWORK value
```

### What to Paste for Exact Fix

```
1. The <button> JSX and its onClick
2. The full handlePurchase / onPurchase function
3. Your WalletProvider setup (the file that wraps the app)
```

---

*Drop the codebase when you're home and we execute this step by step.*
