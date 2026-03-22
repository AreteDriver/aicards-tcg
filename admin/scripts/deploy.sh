#!/bin/bash
# Deploy admin dashboard to Vercel
# Prerequisites:
#   1. Create Supabase project at supabase.com
#   2. Run schema: psql $DATABASE_URL < db/schema.sql
#   3. Set Vercel secrets:
#      vercel secrets add database-url "postgresql://..."
#      vercel secrets add admin-wallet-address "0x..."
#      vercel secrets add jwt-secret "$(openssl rand -hex 32)"
#
# Then run: vercel --prod

echo "=== AI Cards Admin Dashboard ==="
echo ""
echo "Checklist:"
echo "  [ ] Supabase project created"
echo "  [ ] Schema applied (psql \$DATABASE_URL < db/schema.sql)"
echo "  [ ] Vercel secrets configured"
echo "  [ ] ADMIN_API set in index.html"
echo ""
echo "Run: cd admin && vercel --prod"
