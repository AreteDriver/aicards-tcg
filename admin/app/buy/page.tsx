'use client';

import { useState } from 'react';
import { ConnectButton, useCurrentAccount, useSignAndExecuteTransaction } from '@mysten/dapp-kit';
import { Transaction } from '@mysten/sui/transactions';

const PACKAGE_ID = '0x99f91c55ad24367b9fba1000bf43a5e571c2ae096c906fdf2e78fd51243f38b2';
const TREASURY_ID = '0x586cbc4af1eca3cef00e258ad242ddc0d7e4e99ce7a53f18fd60f28a45e3d999';
const MINT_API = 'https://aicards-mint.fly.dev';
const PACK_PRICES: Record<string, number> = { standard: 500_000_000, legendary: 1_000_000_000 };

interface MintedCard {
  card_id: string;
  name: string;
  rarity: string;
  set: string;
  transaction?: string;
  error?: string;
}

export default function BuyPage() {
  const account = useCurrentAccount();
  const { mutateAsync: signAndExecute } = useSignAndExecuteTransaction();
  const [status, setStatus] = useState('');
  const [minting, setMinting] = useState(false);
  const [mintedCards, setMintedCards] = useState<MintedCard[]>([]);

  async function buyPack(packType: string) {
    if (!account) { setStatus('Connect your wallet first'); return; }

    setMinting(true);
    setMintedCards([]);
    setStatus('Building transaction...');

    try {
      const price = PACK_PRICES[packType];

      const tx = new Transaction();
      const [coin] = tx.splitCoins(tx.gas, [price]);
      tx.moveCall({
        target: `${PACKAGE_ID}::payment::buy_pack`,
        arguments: [
          tx.object(TREASURY_ID),
          coin,
          tx.pure.string(packType),
        ],
      });

      setStatus('Approve in your wallet...');

      const result = await signAndExecute({
        transaction: tx,
      });

      const digest = result.digest;
      setStatus('Payment confirmed! Minting NFTs...');

      const res = await fetch(`${MINT_API}/mint/pack`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          sui_address: account.address,
          pack_type: packType,
          payment_digest: digest,
        }),
      });

      const data = await res.json();
      if (data.success) {
        const minted = data.cards.filter((c: MintedCard) => c.transaction);
        setMintedCards(data.cards);
        setStatus(`Minted ${minted.length} cards!`);
      } else {
        setStatus('Mint failed: ' + (data.error || 'Unknown error'));
      }
    } catch (e: unknown) {
      const msg = e instanceof Error ? e.message : String(e);
      if (msg.includes('Rejected') || msg.includes('rejected')) {
        setStatus('Transaction cancelled');
      } else {
        setStatus('Error: ' + msg);
      }
    } finally {
      setMinting(false);
    }
  }

  const RARITY_COLORS: Record<string, string> = {
    MYTHIC: '#ffffff', LEGENDARY: '#c8a84b', RARE: '#9b59d0',
    UNCOMMON: '#4a90d9', COMMON: '#e060a0', JUNK: '#8090a0',
  };

  return (
    <div className="min-h-screen bg-[#0a0a0a] text-[#e0e0e0] flex flex-col items-center p-6">
      <div className="max-w-2xl w-full">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold tracking-[8px] text-[#cc1111] mb-2">AI CARDS</h1>
          <p className="text-xs font-mono tracking-[4px] text-[#555]">BUY PACKS - MINT AS NFTs</p>
        </div>

        {/* Wallet */}
        <div className="flex justify-center mb-8">
          <ConnectButton />
        </div>

        {account && (
          <p className="text-center text-xs font-mono text-[#555] mb-8">
            {account.address.slice(0, 8)}...{account.address.slice(-6)}
          </p>
        )}

        {/* Pack Options */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
          <button
            type="button"
            className="border border-[#2196c8]/30 p-6 text-center hover:-translate-y-1 transition-transform disabled:opacity-50 bg-transparent"
            onClick={() => buyPack('standard')}
            disabled={minting}
          >
            <div className="text-4xl mb-3">&#x1F48E;</div>
            <div className="text-lg font-bold tracking-[3px] text-[#60c8ff] mb-2">BUY PACK</div>
            <p className="text-xs text-[#888] mb-3">5 cards minted as NFTs to your wallet. Sell, trade, collect on-chain.</p>
            <div className="text-xs font-mono tracking-[2px] text-[#555] mb-4">5 CARDS - MINTED ON SUI</div>
            <div className="border border-[#ff3333] bg-[#ff333314] text-[#ff3333] font-mono text-sm tracking-[3px] py-2 px-4">
              BUY - 0.5 SUI
            </div>
            <p className="text-[10px] font-mono text-[#444] mt-2">testnet</p>
          </button>

          <button
            type="button"
            className="border border-[#c8a84b]/30 p-6 text-center hover:-translate-y-1 transition-transform disabled:opacity-50 bg-transparent"
            onClick={() => buyPack('legendary')}
            disabled={minting}
          >
            <div className="text-4xl mb-3">&#x1F451;</div>
            <div className="text-lg font-bold tracking-[3px] text-[#c8a84b] mb-2">BUY REDUNDANCY</div>
            <p className="text-xs text-[#888] mb-3">Guaranteed Legendary. The rarest cards, on-chain forever.</p>
            <div className="text-xs font-mono tracking-[2px] text-[#555] mb-4">5 CARDS - 1 LEGENDARY</div>
            <div className="border border-[#c8a84b] bg-[#c8a84b14] text-[#c8a84b] font-mono text-sm tracking-[3px] py-2 px-4">
              BUY - 1.0 SUI
            </div>
            <p className="text-[10px] font-mono text-[#444] mt-2">testnet - guaranteed legendary NFT</p>
          </button>
        </div>

        {/* Status */}
        {status && (
          <div className="text-center text-sm font-mono text-[#888] mb-6 p-3 border border-[#222]">
            {status}
          </div>
        )}

        {/* Minted Cards */}
        {mintedCards.length > 0 && (
          <div className="border border-[#222] p-4 mb-6">
            <div className="text-[9px] font-mono tracking-[3px] text-[#888] mb-4 pb-2 border-b border-[#1a1a1a]">MINTED CARDS</div>
            {mintedCards.map((card, i) => (
              <div key={i} className="flex items-center justify-between text-xs font-mono mb-2">
                <span style={{ color: RARITY_COLORS[card.rarity] || '#888' }}>{card.name}</span>
                <span className="text-[#555]">{card.rarity}</span>
                {card.transaction ? (
                  <a
                    href={`https://suiscan.xyz/testnet/tx/${card.transaction}`}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-[#60c8ff] hover:underline"
                  >
                    View
                  </a>
                ) : (
                  <span className="text-[#ff3333]">Failed</span>
                )}
              </div>
            ))}
          </div>
        )}

        {/* Back link */}
        <div className="text-center">
          <a href="https://aicards.fun" className="text-xs font-mono text-[#555] hover:text-[#888] tracking-[2px]">
            BACK TO AICARDS.FUN
          </a>
        </div>
      </div>
    </div>
  );
}
