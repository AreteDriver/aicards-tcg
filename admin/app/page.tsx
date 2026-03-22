'use client';

import { useState, useEffect, useCallback } from 'react';
import { ConnectButton, useCurrentAccount, useSignPersonalMessage } from '@mysten/dapp-kit';

interface Metrics {
  dau: number;
  wau: number;
  mau: number;
  packsToday: number;
  cardsToday: number;
  raidsToday: number;
  rarity: Array<{ rarity: string; count: string }>;
  packs: Array<{ set_name: string; count: string }>;
  topCards: Array<{ card_id: string; card_name: string; rarity: string; count: string }>;
  goals: Array<{ goal_type: string; goal_id: string; count: string }>;
  shares: { total: number; byPlatform: Array<{ platform: string; count: string }>; topCards: Array<{ card_id: string; card_name: string; rarity: string; count: string }> };
  raids: { total: number; topBosses: Array<{ boss_id: string; boss_tier: string; count: string }>; byTier: Array<{ boss_tier: string; count: string }> };
}

const RARITY_COLORS: Record<string, string> = {
  MYTHIC: '#ffffff',
  LEGENDARY: '#c8a84b',
  RARE: '#9b59d0',
  UNCOMMON: '#4a90d9',
  COMMON: '#f080c0',
  JUNK: '#667080',
};

const TIER_COLORS: Record<string, string> = {
  APEX: '#ff3333',
  ELITE: '#ff8800',
  STANDARD: '#666666',
};

export default function AdminDashboard() {
  const [token, setToken] = useState<string | null>(null);
  const [metrics, setMetrics] = useState<Metrics | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [lastRefresh, setLastRefresh] = useState<Date | null>(null);

  useEffect(() => {
    const saved = localStorage.getItem('adminToken');
    if (saved) setToken(saved);
  }, []);

  const fetchMetrics = useCallback(async () => {
    if (!token) return;
    setLoading(true);
    setError(null);
    try {
      const res = await fetch('/api/admin/metrics', {
        headers: { Authorization: `Bearer ${token}` },
      });
      if (res.status === 403) {
        setToken(null);
        localStorage.removeItem('adminToken');
        setError('Session expired');
        return;
      }
      const data = await res.json();
      setMetrics(data);
      setLastRefresh(new Date());
    } catch {
      setError('Failed to fetch metrics');
    } finally {
      setLoading(false);
    }
  }, [token]);

  useEffect(() => {
    if (token) fetchMetrics();
  }, [token, fetchMetrics]);

  useEffect(() => {
    if (!token) return;
    const interval = setInterval(fetchMetrics, 60000);
    return () => clearInterval(interval);
  }, [token, fetchMetrics]);

  if (!token) return <LoginScreen onLogin={(t) => { setToken(t); localStorage.setItem('adminToken', t); }} />;

  return (
    <div className="min-h-screen bg-[#0a0a0a] text-[#e0e0e0] p-6">
      <header className="flex items-center justify-between mb-8 border-b border-[#222] pb-4">
        <div>
          <h1 className="text-2xl font-bold tracking-[6px] text-[#cc1111]">AICARDS ADMIN</h1>
          <p className="text-xs text-[#555] mt-1 font-mono tracking-wider">
            {lastRefresh ? `Last refresh: ${lastRefresh.toLocaleTimeString()}` : 'Loading...'}
          </p>
        </div>
        <div className="flex items-center gap-4">
          <button onClick={fetchMetrics} disabled={loading} className="text-xs font-mono px-3 py-1 border border-[#333] hover:border-[#c8a84b] transition-colors">
            {loading ? 'REFRESHING...' : 'REFRESH'}
          </button>
          <button onClick={() => { setToken(null); localStorage.removeItem('adminToken'); }} className="text-xs font-mono px-3 py-1 border border-[#333] text-[#666] hover:text-[#ff3333] hover:border-[#ff3333] transition-colors">
            LOGOUT
          </button>
        </div>
      </header>

      {error && <div className="text-[#ff3333] text-sm font-mono mb-4">{error}</div>}

      {metrics ? (
        <div className="grid gap-6">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <KPICard label="DAU" value={metrics.dau} />
            <KPICard label="PACKS TODAY" value={metrics.packsToday} />
            <KPICard label="CARDS TODAY" value={metrics.cardsToday} />
            <KPICard label="RAIDS TODAY" value={metrics.raidsToday} />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <KPICard label="WAU" value={metrics.wau} />
            <KPICard label="MAU" value={metrics.mau} />
            <KPICard label="SHARES TODAY" value={metrics.shares.total} />
          </div>

          <Panel title="RARITY DISTRIBUTION (TODAY)">
            {metrics.rarity.length === 0 ? <Empty /> : metrics.rarity.map((r) => {
              const total = metrics.rarity.reduce((sum, x) => sum + parseInt(x.count), 0);
              const pct = total > 0 ? (parseInt(r.count) / total * 100).toFixed(1) : '0';
              return (
                <div key={r.rarity} className="flex items-center gap-3 mb-2">
                  <span className="w-24 text-xs font-mono" style={{ color: RARITY_COLORS[r.rarity] || '#888' }}>{r.rarity}</span>
                  <div className="flex-1 h-3 bg-[#1a1a1a] rounded overflow-hidden">
                    <div className="h-full rounded" style={{ width: `${pct}%`, background: RARITY_COLORS[r.rarity] || '#888' }} />
                  </div>
                  <span className="text-xs font-mono text-[#888] w-16 text-right">{pct}%</span>
                  <span className="text-xs font-mono text-[#555] w-12 text-right">{r.count}</span>
                </div>
              );
            })}
          </Panel>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <Panel title="PACKS BY SET (TODAY)">
              {metrics.packs.length === 0 ? <Empty /> : metrics.packs.map((p) => (
                <div key={p.set_name} className="flex justify-between text-xs font-mono mb-1">
                  <span className="text-[#aaa]">{p.set_name.toUpperCase()}</span>
                  <span className="text-[#c8a84b]">{p.count}</span>
                </div>
              ))}
            </Panel>

            <Panel title="TOP CARDS PULLED (TODAY)">
              {metrics.topCards.length === 0 ? <Empty /> : metrics.topCards.map((c, i) => (
                <div key={c.card_id} className="flex items-center gap-2 text-xs font-mono mb-1">
                  <span className="text-[#555] w-4">{i + 1}.</span>
                  <span style={{ color: RARITY_COLORS[c.rarity] || '#888' }}>{c.card_name}</span>
                  <span className="ml-auto text-[#888]">{c.count}</span>
                </div>
              ))}
            </Panel>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <Panel title="RAID ACTIVITY (TODAY)">
              <div className="text-xs font-mono mb-3">
                <span className="text-[#888]">Total Raids: </span>
                <span className="text-[#ff8800]">{metrics.raids.total}</span>
              </div>
              {metrics.raids.byTier.map((t) => (
                <div key={t.boss_tier} className="flex justify-between text-xs font-mono mb-1">
                  <span style={{ color: TIER_COLORS[t.boss_tier] || '#888' }}>{t.boss_tier}</span>
                  <span className="text-[#888]">{t.count}</span>
                </div>
              ))}
              {metrics.raids.topBosses.length > 0 && (
                <div className="mt-3 pt-3 border-t border-[#1a1a1a]">
                  <div className="text-[8px] tracking-[3px] text-[#555] mb-2">MOST DEFEATED</div>
                  {metrics.raids.topBosses.map((b) => (
                    <div key={b.boss_id} className="flex justify-between text-xs font-mono mb-1">
                      <span className="text-[#aaa]">{b.boss_id.replace(/_/g, ' ').toUpperCase()}</span>
                      <span className="text-[#888]">{b.count}</span>
                    </div>
                  ))}
                </div>
              )}
            </Panel>

            <Panel title="CARD SHARES (TODAY)">
              <div className="text-xs font-mono mb-3">
                <span className="text-[#888]">Total Shares: </span>
                <span className="text-[#4a90d9]">{metrics.shares.total}</span>
              </div>
              {metrics.shares.byPlatform.map((p) => (
                <div key={p.platform} className="flex justify-between text-xs font-mono mb-1">
                  <span className="text-[#aaa]">{p.platform.toUpperCase()}</span>
                  <span className="text-[#888]">{p.count}</span>
                </div>
              ))}
              {metrics.shares.topCards.length > 0 && (
                <div className="mt-3 pt-3 border-t border-[#1a1a1a]">
                  <div className="text-[8px] tracking-[3px] text-[#555] mb-2">MOST SHARED</div>
                  {metrics.shares.topCards.map((c) => (
                    <div key={c.card_id} className="flex items-center gap-2 text-xs font-mono mb-1">
                      <span style={{ color: RARITY_COLORS[c.rarity] || '#888' }}>{c.card_name}</span>
                      <span className="ml-auto text-[#888]">{c.count}</span>
                    </div>
                  ))}
                </div>
              )}
            </Panel>
          </div>

          <Panel title="GOAL COMPLETIONS (TODAY)">
            {metrics.goals.length === 0 ? <Empty /> : metrics.goals.map((g) => (
              <div key={`${g.goal_type}-${g.goal_id}`} className="flex justify-between text-xs font-mono mb-1">
                <span className="text-[#aaa]">{g.goal_type.toUpperCase()}: {g.goal_id}</span>
                <span className="text-[#4a4]">{g.count} completed</span>
              </div>
            ))}
          </Panel>
        </div>
      ) : (
        <div className="text-center text-[#555] font-mono text-sm mt-20">
          {loading ? 'Loading metrics...' : 'No data'}
        </div>
      )}
    </div>
  );
}

function LoginScreen({ onLogin }: { onLogin: (token: string) => void }) {
  const [status, setStatus] = useState('');
  const account = useCurrentAccount();
  const { mutateAsync: signMessage } = useSignPersonalMessage();

  async function handleSign() {
    if (!account) {
      setStatus('Connect your wallet first');
      return;
    }
    setStatus('Signing...');
    try {
      const message = `AICards Admin Login - ${Date.now()}`;
      const { signature } = await signMessage({
        message: new TextEncoder().encode(message),
      });
      setStatus('Verifying...');
      const res = await fetch('/api/admin/auth', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ address: account.address, signature, message }),
      });
      if (!res.ok) {
        setStatus('Not authorized — wallet does not match admin address');
        return;
      }
      const { token } = await res.json();
      onLogin(token);
    } catch (e: unknown) {
      setStatus(`Error: ${e instanceof Error ? e.message : 'Unknown error'}`);
    }
  }

  return (
    <div className="min-h-screen bg-[#0a0a0a] flex items-center justify-center">
      <div className="text-center">
        <h1 className="text-3xl font-bold tracking-[8px] text-[#cc1111] mb-2">AICARDS</h1>
        <p className="text-xs font-mono tracking-[4px] text-[#555] mb-12">ADMIN DASHBOARD</p>
        <div className="mb-6">
          <ConnectButton />
        </div>
        {account && (
          <div>
            <p className="text-xs font-mono text-[#555] mb-4">{account.address.slice(0, 8)}...{account.address.slice(-6)}</p>
            <button
              onClick={handleSign}
              className="px-8 py-3 border border-[#c8a84b] text-[#c8a84b] font-mono text-sm tracking-[3px] hover:bg-[#c8a84b] hover:text-black transition-colors"
            >
              SIGN IN AS ADMIN
            </button>
          </div>
        )}
        {status && <p className="mt-6 text-xs font-mono text-[#888]">{status}</p>}
      </div>
    </div>
  );
}

function KPICard({ label, value }: { label: string; value: number }) {
  return (
    <div className="border border-[#222] p-4">
      <div className="text-2xl font-bold text-[#e0e0e0]">{value.toLocaleString()}</div>
      <div className="text-[8px] font-mono tracking-[3px] text-[#555] mt-1">{label}</div>
    </div>
  );
}

function Panel({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <div className="border border-[#222] p-4">
      <div className="text-[9px] font-mono tracking-[3px] text-[#888] mb-4 pb-2 border-b border-[#1a1a1a]">{title}</div>
      {children}
    </div>
  );
}

function Empty() {
  return <div className="text-xs font-mono text-[#333]">No data yet</div>;
}
