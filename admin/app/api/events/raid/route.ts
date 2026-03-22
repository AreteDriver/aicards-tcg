import { NextRequest, NextResponse } from 'next/server';
import pool from '@/lib/db';

export async function POST(req: NextRequest) {
  const { user_address, boss_id, boss_tier, pack_reward_set } = await req.json();
  if (!user_address || !boss_id) {
    return NextResponse.json({ error: 'Missing fields' }, { status: 400 });
  }
  await pool.query(
    'INSERT INTO raid_events (user_address, boss_id, boss_tier, pack_reward_set) VALUES ($1, $2, $3, $4)',
    [user_address, boss_id, boss_tier || '', pack_reward_set || '']
  );
  return NextResponse.json({ ok: true });
}
