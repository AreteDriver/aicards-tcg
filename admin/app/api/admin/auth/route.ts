import { NextRequest, NextResponse } from 'next/server';
import { verifyAdminWallet, signAdminToken } from '@/lib/adminAuth';

export async function POST(req: NextRequest) {
  const { address, signature, message } = await req.json();
  if (!address || !signature || !message) {
    return NextResponse.json({ error: 'Missing fields' }, { status: 400 });
  }
  const isAdmin = await verifyAdminWallet(address, signature, message);
  if (!isAdmin) {
    return NextResponse.json({ error: 'Not authorized' }, { status: 403 });
  }
  const token = signAdminToken(address);
  return NextResponse.json({ token });
}
