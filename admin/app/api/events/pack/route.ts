import { NextRequest, NextResponse } from 'next/server';
import pool from '@/lib/db';

const CORS_HEADERS = {
  'Access-Control-Allow-Origin': 'https://aicards.fun',
  'Access-Control-Allow-Methods': 'POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type',
};

export async function OPTIONS() {
  return new Response(null, { status: 204, headers: CORS_HEADERS });
}

export async function POST(req: NextRequest) {
  const { user_address, set_name } = await req.json();
  if (!user_address || !set_name) {
    return NextResponse.json({ error: 'Missing fields' }, { status: 400, headers: CORS_HEADERS });
  }
  await pool.query(
    'INSERT INTO pack_events (user_address, set_name) VALUES ($1, $2)',
    [user_address, set_name]
  );
  // Upsert session
  await pool.query(
    'INSERT INTO user_sessions (user_address) VALUES ($1) ON CONFLICT (user_address, session_date) DO NOTHING',
    [user_address]
  );
  return NextResponse.json({ ok: true }, { headers: CORS_HEADERS });
}
