import { NextRequest, NextResponse } from 'next/server';
import { verifyAdminToken } from '@/lib/adminAuth';
import { getOverview, getWAU, getMAU, getRarityDistribution, getPacksBySet, getTopCards, getGoalCompletions, getShareMetrics, getRaidMetrics } from '@/lib/metrics';

function checkAuth(req: NextRequest) {
  const token = req.headers.get('authorization')?.replace('Bearer ', '');
  if (!token) return null;
  return verifyAdminToken(token);
}

export async function GET(req: NextRequest) {
  const admin = checkAuth(req);
  if (!admin) return NextResponse.json({ error: 'Unauthorized' }, { status: 403 });

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
  });
}
