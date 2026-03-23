import { verifyPersonalMessageSignature } from '@mysten/sui/verify';
import jwt from 'jsonwebtoken';

const ADMIN_WALLET_ADDRESS = process.env.ADMIN_WALLET_ADDRESS!;
const JWT_SECRET = process.env.JWT_SECRET!;

export async function verifyAdminWallet(
  address: string,
  signature: string,
  message: string
): Promise<boolean> {
  console.log('[admin-auth] address:', address);
  console.log('[admin-auth] ADMIN_WALLET_ADDRESS:', ADMIN_WALLET_ADDRESS);
  console.log('[admin-auth] match:', address.toLowerCase() === ADMIN_WALLET_ADDRESS.toLowerCase());
  if (address.toLowerCase() !== ADMIN_WALLET_ADDRESS.toLowerCase()) return false;
  try {
    const publicKey = await verifyPersonalMessageSignature(
      new TextEncoder().encode(message),
      signature
    );
    const derivedAddress = publicKey.toSuiAddress();
    console.log('[admin-auth] derivedAddress:', derivedAddress);
    console.log('[admin-auth] wallet address:', address);
    // Normalize: both to lowercase, ensure 0x prefix
    const norm = (a: string) => a.toLowerCase().replace(/^0x/, '');
    return norm(derivedAddress) === norm(address);
  } catch (e) {
    console.error('[admin-auth] verify error:', e);
    return false;
  }
}

export function signAdminToken(address: string): string {
  return jwt.sign({ address, role: 'admin' }, JWT_SECRET, { expiresIn: '8h' });
}

export function verifyAdminToken(token: string): { address: string; role: string } | null {
  try {
    const payload = jwt.verify(token, JWT_SECRET) as { address: string; role: string };
    if (payload.role !== 'admin') return null;
    return payload;
  } catch {
    return null;
  }
}
