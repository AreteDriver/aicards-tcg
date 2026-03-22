import pool from './db';

export async function getOverview() {
  const [dau, packs, cards, raids] = await Promise.all([
    pool.query(`SELECT COUNT(DISTINCT user_address) as count FROM user_sessions WHERE session_date = CURRENT_DATE`),
    pool.query(`SELECT COUNT(*) as count FROM pack_events WHERE opened_at >= CURRENT_DATE`),
    pool.query(`SELECT COUNT(*) as count FROM card_pull_events WHERE pulled_at >= CURRENT_DATE`),
    pool.query(`SELECT COUNT(*) as count FROM raid_events WHERE completed_at >= CURRENT_DATE`),
  ]);
  return {
    dau: parseInt(dau.rows[0]?.count || '0'),
    packsToday: parseInt(packs.rows[0]?.count || '0'),
    cardsToday: parseInt(cards.rows[0]?.count || '0'),
    raidsToday: parseInt(raids.rows[0]?.count || '0'),
  };
}

export async function getWAU() {
  const result = await pool.query(
    `SELECT COUNT(DISTINCT user_address) as count FROM user_sessions WHERE session_date >= CURRENT_DATE - INTERVAL '7 days'`
  );
  return parseInt(result.rows[0]?.count || '0');
}

export async function getMAU() {
  const result = await pool.query(
    `SELECT COUNT(DISTINCT user_address) as count FROM user_sessions WHERE session_date >= CURRENT_DATE - INTERVAL '30 days'`
  );
  return parseInt(result.rows[0]?.count || '0');
}

export async function getRarityDistribution(period: 'today' | 'all' = 'today') {
  const where = period === 'today' ? 'WHERE pulled_at >= CURRENT_DATE' : '';
  const result = await pool.query(
    `SELECT rarity, COUNT(*) as count FROM card_pull_events ${where} GROUP BY rarity ORDER BY count DESC`
  );
  return result.rows;
}

export async function getPacksBySet(period: 'today' | 'week' | 'all' = 'today') {
  const intervals: Record<string, string> = {
    today: 'WHERE opened_at >= CURRENT_DATE',
    week: "WHERE opened_at >= CURRENT_DATE - INTERVAL '7 days'",
    all: '',
  };
  const result = await pool.query(
    `SELECT set_name, COUNT(*) as count FROM pack_events ${intervals[period]} GROUP BY set_name ORDER BY count DESC`
  );
  return result.rows;
}

export async function getTopCards(limit = 10) {
  const result = await pool.query(
    `SELECT card_id, card_name, rarity, COUNT(*) as count FROM card_pull_events WHERE pulled_at >= CURRENT_DATE GROUP BY card_id, card_name, rarity ORDER BY count DESC LIMIT $1`,
    [limit]
  );
  return result.rows;
}

export async function getGoalCompletions(period: 'today' | 'week' = 'today') {
  const interval = period === 'today' ? 'CURRENT_DATE' : "CURRENT_DATE - INTERVAL '7 days'";
  const result = await pool.query(
    `SELECT goal_type, goal_id, COUNT(*) as count FROM goal_completions WHERE completed_at >= ${interval} GROUP BY goal_type, goal_id ORDER BY goal_type, count DESC`
  );
  return result.rows;
}

export async function getShareMetrics(period: 'today' | 'week' | 'all' = 'today') {
  const intervals: Record<string, string> = {
    today: 'WHERE shared_at >= CURRENT_DATE',
    week: "WHERE shared_at >= CURRENT_DATE - INTERVAL '7 days'",
    all: '',
  };
  const [total, byPlatform, topCards] = await Promise.all([
    pool.query(`SELECT COUNT(*) as count FROM card_share_events ${intervals[period]}`),
    pool.query(`SELECT platform, COUNT(*) as count FROM card_share_events ${intervals[period]} GROUP BY platform`),
    pool.query(`SELECT card_id, card_name, rarity, COUNT(*) as count FROM card_share_events ${intervals[period]} GROUP BY card_id, card_name, rarity ORDER BY count DESC LIMIT 5`),
  ]);
  return {
    total: parseInt(total.rows[0]?.count || '0'),
    byPlatform: byPlatform.rows,
    topCards: topCards.rows,
  };
}

export async function getRaidMetrics() {
  const [total, byBoss, byTier] = await Promise.all([
    pool.query(`SELECT COUNT(*) as count FROM raid_events WHERE completed_at >= CURRENT_DATE`),
    pool.query(`SELECT boss_id, boss_tier, COUNT(*) as count FROM raid_events WHERE completed_at >= CURRENT_DATE GROUP BY boss_id, boss_tier ORDER BY count DESC LIMIT 5`),
    pool.query(`SELECT boss_tier, COUNT(*) as count FROM raid_events WHERE completed_at >= CURRENT_DATE GROUP BY boss_tier ORDER BY count DESC`),
  ]);
  return {
    total: parseInt(total.rows[0]?.count || '0'),
    topBosses: byBoss.rows,
    byTier: byTier.rows,
  };
}
