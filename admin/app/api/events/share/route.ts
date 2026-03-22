import { NextRequest, NextResponse } from 'next/server';
import pool from '@/lib/db';

export async function POST(req: NextRequest) {
  const { user_address, card_id, card_name, rarity, set_name, platform } = await req.json();
  if (!user_address || !card_id || !platform) {
    return NextResponse.json({ error: 'Missing fields' }, { status: 400 });
  }
  await pool.query(
    'INSERT INTO card_share_events (user_address, card_id, card_name, rarity, set_name, platform) VALUES ($1, $2, $3, $4, $5, $6)',
    [user_address, card_id, card_name || '', rarity || '', set_name || '', platform]
  );
  return NextResponse.json({ ok: true });
}
