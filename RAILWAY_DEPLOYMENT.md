# Railway Deployment Guide

## Current Status

✅ **All code is committed and ready** (commit `c82910b`)
- RapidAPI integration complete
- Railway configuration simplified
- All changes pushed to GitHub main branch

❌ **Railway backend needs manual redeploy**
- Currently running old commit (29f6d34c) with mock database
- Needs to deploy latest commit with RapidAPI code

## Quick Deployment (2 Options)

### Option 1: Railway Web Dashboard (Recommended)

1. Open https://railway.app/
2. Navigate to your **uspto-backend** project
3. Click on the backend service
4. Click the **"..."** menu (three dots)
5. Select **"Redeploy"**
6. Wait for build to complete (~2-3 minutes)

### Option 2: Railway CLI

```bash
cd "/Users/tomsuharto/Documents/Obsidian Vault/Claude Code/USPTO"
railway redeploy --yes
```

Note: This requires Railway CLI to be linked to the correct service.

## Verify Deployment

After Railway finishes deploying, test the backend:

```bash
# Test the API directly
curl -X POST 'https://uspto-backend-production.up.railway.app/api/v1/analysis/analyze' \
  -H 'Content-Type: application/json' \
  -d '{"query": "Nike"}' | jq '.results[0:3]'
```

**Expected:** Should return real Nike trademarks (not the 3 mock ones: 88234567, 88234568, 88234569)

Then test the full frontend:

```bash
python3 test_deployment.py
```

**Expected:** Should show "✅ SUCCESS: Showing real trademark data from RapidAPI!"

## What Changed

The backend was updated to use **RapidAPI** for real-time trademark searches instead of a PostgreSQL database:

### Before (Mock Data)
- PostgreSQL with 3 test trademarks
- Limited to demo data
- Database approach failed due to size limits (12.7M+ trademarks)

### After (Real Data)
- RapidAPI for trademark searches
- Complete USPTO database access
- TSDR API for detailed trademark info (on-demand)

## Configuration Files

- `/railway.json` - Railway deployment configuration
- `/backend/app/services/uspto.py` - RapidAPI integration
- `/backend/app/config.py` - Environment variables (DATABASE_URL now optional)

## Troubleshooting

### Build fails with "can't find app"
Railway configuration specifies `cd backend && uvicorn ...` in the start command. This should be handled automatically by Nixpacks.

### Still showing mock results after deploy
1. Check Railway logs: `railway logs`
2. Look for "🔍 RapidAPI search for..." messages (not "Database search")
3. Verify deployment used latest commit (not 29f6d34c)

### Environment variables missing
Ensure Railway has these variables set:
- `RAPIDAPI_KEY`
- `RAPIDAPI_HOST` (should be: uspto-trademark.p.rapidapi.com)
- `ANTHROPIC_API_KEY`
- `USPTO_API_KEY`
- `DATABASE_URL` (optional - can be empty)

## Support

If deployment continues to fail, check Railway build logs for specific errors:
```bash
railway logs --deployment
```
