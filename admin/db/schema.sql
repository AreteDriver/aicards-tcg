-- AI Cards Admin — Metrics Tables

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
  rarity TEXT NOT NULL,
  set_name TEXT NOT NULL,
  pulled_at TIMESTAMPTZ DEFAULT NOW()
);

-- Track raid completions
CREATE TABLE raid_events (
  id SERIAL PRIMARY KEY,
  user_address TEXT NOT NULL,
  boss_id TEXT NOT NULL,
  boss_tier TEXT NOT NULL,
  pack_reward_set TEXT NOT NULL,
  completed_at TIMESTAMPTZ DEFAULT NOW()
);

-- Track goal completions
CREATE TABLE goal_completions (
  id SERIAL PRIMARY KEY,
  user_address TEXT NOT NULL,
  goal_type TEXT NOT NULL,
  goal_id TEXT NOT NULL,
  completed_at TIMESTAMPTZ DEFAULT NOW()
);

-- Track reward claims (prevent double-claiming)
CREATE TABLE reward_claims (
  id SERIAL PRIMARY KEY,
  user_address TEXT NOT NULL,
  reward_type TEXT NOT NULL,
  period_key TEXT NOT NULL,
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

-- Track card shares
CREATE TABLE card_share_events (
  id SERIAL PRIMARY KEY,
  user_address TEXT NOT NULL,
  card_id TEXT NOT NULL,
  card_name TEXT NOT NULL,
  rarity TEXT NOT NULL,
  set_name TEXT NOT NULL,
  platform TEXT NOT NULL,
  shared_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_card_pulls_pulled_at ON card_pull_events(pulled_at);
CREATE INDEX idx_card_pulls_rarity ON card_pull_events(rarity);
CREATE INDEX idx_pack_events_opened_at ON pack_events(opened_at);
CREATE INDEX idx_raid_events_completed_at ON raid_events(completed_at);
CREATE INDEX idx_card_shares_shared_at ON card_share_events(shared_at);
CREATE INDEX idx_card_shares_card_id ON card_share_events(card_id);
CREATE INDEX idx_card_shares_platform ON card_share_events(platform);
