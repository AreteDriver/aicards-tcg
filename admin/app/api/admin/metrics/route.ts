import { NextRequest, NextResponse } from 'next/server';
import { verifyAdminToken } from '@/lib/adminAuth';
import { getOverview, getWAU, getMAU, getRarityDistribution, getPacksBySet, getTopCards, getGoalCompletions, getShareMetrics, getRaidMetrics } from '@/lib/metrics';

const CORS_HEADERS = {
  'Access-Control-Allow-Origin': 'https://aicards.fun',
  'Access-Control-Allow-Methods': 'GET, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type, Authorization',
};

export async function OPTIONS() {
  return new Response(null, { status: 204, headers: CORS_HEADERS });
}

function getAllowedOrigin(req: NextRequest): Record<string, string> {
  const origin = req.headers.get('origin') || '';
  const allowed = ['https://aicards.fun', 'http://localhost:3000'];
  if (allowed.includes(origin)) {
    return { ...CORS_HEADERS, 'Access-Control-Allow-Origin': origin };
  }
  return CORS_HEADERS;
}

function checkAuth(req: NextRequest) {
  const token = req.headers.get('authorization')?.replace('Bearer ', '');
  if (!token) return null;
  return verifyAdminToken(token);
}

export async function GET(req: NextRequest) {
  const headers = getAllowedOrigin(req);
  const admin = checkAuth(req);
  if (!admin) return NextResponse.json({ error: 'Unauthorized' }, { status: 403, headers });

  const [overview, wau, mau, rarity, packs, topCards, goals, shares, raids] = await Promise.all([
    getOverview(),
    getWAU(),
    getMAU(),
    getRarityDistribution(),
    getPacksBySet(),
    getTopCards(),
    getGoalCompletions(),
    getShareMetrics(),
    getRaidMetrics(),
  ]);

  return NextResponse.json({
    ...overview,
    wau,
    mau,
    rarity,
    packs,
    topCards,
    goals,
    shares,
    raids,
  }, { headers });
}
