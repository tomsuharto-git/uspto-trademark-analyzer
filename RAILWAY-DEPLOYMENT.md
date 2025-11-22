# Railway Deployment Guide

## Step-by-Step Backend Deployment

### 1. Login to Railway

Open your terminal and run:

```bash
railway login
```

This will open your browser. Login with:
- GitHub (recommended)
- Email
- Google

### 2. Initialize Railway Project

```bash
cd "/Users/tomsuharto/Documents/Obsidian Vault/Claude Code/USPTO/backend"
railway init
```

When prompted:
- **Create new project?** Yes
- **Project name:** uspto-trademark-analyzer-backend (or your choice)
- **Environment:** production

### 3. Link to GitHub (Optional but Recommended)

```bash
railway link
```

This enables auto-deploy on git push.

### 4. Set Environment Variables

```bash
# USPTO API Key
railway variables set USPTO_API_KEY=szbcdzcfpygkhqpzigiuoqapzfgiay

# Anthropic API Key (get from backend/.env file)
railway variables set ANTHROPIC_API_KEY=your-anthropic-api-key-from-env-file

# Environment
railway variables set ENVIRONMENT=production
railway variables set DEBUG=false

# CORS Origins (your Vercel frontend URL)
railway variables set CORS_ORIGINS=https://frontend-i6hvfo09t-tomsuharto-3884s-projects.vercel.app
```

### 5. Deploy Backend

```bash
railway up
```

This will:
- Upload your code
- Install dependencies from requirements.txt
- Start the FastAPI server
- Give you a public URL

### 6. Get Your Backend URL

```bash
railway domain
```

Or check the Railway dashboard at https://railway.app/dashboard

Your backend URL will look like:
```
https://uspto-trademark-analyzer-backend-production.up.railway.app
```

### 7. Update Frontend Environment Variable

Once you have your backend URL, update Vercel:

```bash
cd ../frontend

# Set production environment variable
vercel env add NEXT_PUBLIC_API_URL production
# When prompted, enter: https://YOUR-BACKEND-URL.railway.app/api/v1

# Redeploy frontend with new env var
vercel --prod
```

## Verification Steps

### Test Backend

Visit your backend URL + `/docs`:
```
https://YOUR-BACKEND-URL.railway.app/docs
```

You should see the FastAPI Swagger documentation.

Test the health endpoint:
```
https://YOUR-BACKEND-URL.railway.app/health
```

Should return:
```json
{"status": "healthy", "environment": "production"}
```

### Test Full Application

1. Visit your Vercel frontend URL
2. Search for "ACME"
3. Wait for AI analysis
4. Verify results display correctly

## Railway Dashboard

Access your project at: https://railway.app/dashboard

From there you can:
- View logs
- Monitor resources
- Update environment variables
- Check deployments
- View metrics

## Costs

**Free Trial:**
- $5 credit (about 500 hours)
- No credit card required initially

**After Trial:**
- ~$5/month for this app
- Pay only for what you use

## Troubleshooting

### Build Fails

Check logs:
```bash
railway logs
```

Common fixes:
- Verify requirements.txt is correct
- Check Python version in runtime.txt
- Review build logs for specific errors

### App Won't Start

1. Check start command in railway.json
2. Verify PORT environment variable is used
3. Check logs: `railway logs`

### Environment Variables Not Working

```bash
# List all variables
railway variables

# Update a variable
railway variables set KEY=VALUE
```

### CORS Errors

Update CORS_ORIGINS to include your Vercel domain:

```bash
railway variables set CORS_ORIGINS=https://frontend-i6hvfo09t-tomsuharto-3884s-projects.vercel.app,https://your-custom-domain.com
```

## Automatic Deployments

If you linked to GitHub:
- Every push to `main` branch auto-deploys
- View deployment status in Railway dashboard
- Rollback available if needed

## Custom Domain (Optional)

1. Go to Railway dashboard
2. Select your project
3. Settings → Domains
4. Add custom domain
5. Update DNS records as instructed

## Monitoring

Railway provides:
- CPU usage graphs
- Memory usage
- Request logs
- Deployment history
- Crash reports

## Need Help?

- Railway Docs: https://docs.railway.app/
- Railway Discord: https://discord.gg/railway
- Check logs: `railway logs --follow`

---

## Quick Reference Commands

```bash
# Login
railway login

# Initialize project
railway init

# Deploy
railway up

# View logs
railway logs
railway logs --follow

# Set environment variable
railway variables set KEY=VALUE

# List variables
railway variables

# Get domain
railway domain

# Check status
railway status

# Open dashboard
railway open
```
