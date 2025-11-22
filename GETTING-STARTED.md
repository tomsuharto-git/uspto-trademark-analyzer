# Getting Started - USPTO Trademark Risk Analyzer

This guide will walk you through setting up and running the USPTO Trademark Risk Analyzer for the first time.

## Prerequisites

Before you begin, make sure you have:

- ✅ **Python 3.11 or higher** - Check with `python --version`
- ✅ **Node.js 18 or higher** - Check with `node --version`
- ✅ **USPTO API Key** - You already have: `szbcdzcfpygkhqpzigiuoqapzfgiay`
- ⚠️ **Anthropic API Key** - Get one at https://console.anthropic.com/

## Step-by-Step Setup

### Step 1: Get Your Anthropic API Key

1. Go to https://console.anthropic.com/
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key (starts with `sk-ant-...`)

### Step 2: Set Up the Backend

Open a terminal and run:

```bash
# Navigate to backend directory
cd /Users/tomsuharto/Documents/Obsidian\ Vault/Claude\ Code/USPTO/backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies (takes 1-2 minutes)
pip install -r requirements.txt
```

**Configure your API keys:**

The `.env` file already has your USPTO key. You just need to add your Claude API key:

```bash
# Open .env file in your editor
# Replace "your-claude-api-key-here" with your actual key
```

Or use this command:

```bash
# Replace YOUR_KEY with your actual Anthropic API key
sed -i '' 's/your-claude-api-key-here/YOUR_KEY/g' .env
```

### Step 3: Start the Backend

```bash
# Make sure you're in the backend directory with venv activated
uvicorn app.main:app --reload --port 8000
```

You should see:

```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

**Test it:** Open http://localhost:8000/docs in your browser. You should see the API documentation.

**Leave this terminal running!**

### Step 4: Set Up the Frontend

Open a **new terminal** window:

```bash
# Navigate to frontend directory
cd /Users/tomsuharto/Documents/Obsidian\ Vault/Claude\ Code/USPTO/frontend

# Install dependencies (takes 2-3 minutes)
npm install
```

The `.env.local` file is already configured to connect to your backend.

### Step 5: Start the Frontend

```bash
# Make sure you're in the frontend directory
npm run dev
```

You should see:

```
  ▲ Next.js 14.1.0
  - Local:        http://localhost:3000
  - Ready in 2.5s
```

**Leave this terminal running too!**

### Step 6: Use the App

1. Open http://localhost:3000 in your browser
2. You should see the USPTO Trademark Risk Analyzer homepage
3. Try searching for "ACME" or "TECH PRO"
4. Wait for the AI analysis (takes 5-10 seconds)
5. Review the results!

## Troubleshooting

### Backend Issues

**"Module not found" errors:**
```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

**"Invalid API key" from USPTO:**
```bash
# Verify the key in .env file
cat .env | grep USPTO_API_KEY
# Should show: USPTO_API_KEY=szbcdzcfpygkhqpzigiuoqapzfgiay
```

**"Invalid API key" from Anthropic:**
```bash
# Check your Claude API key
cat .env | grep ANTHROPIC_API_KEY
# Make sure it's not "your-claude-api-key-here"
```

### Frontend Issues

**"Cannot connect to backend":**
- Make sure backend is running on http://localhost:8000
- Check backend terminal for error messages
- Verify `.env.local` has: `NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1`

**"npm install" fails:**
```bash
# Clear cache and try again
rm -rf node_modules package-lock.json
npm cache clean --force
npm install
```

**Port 3000 already in use:**
```bash
# Use a different port
npm run dev -- -p 3001
# Then open http://localhost:3001
```

## Quick Test

Once both servers are running, test the full stack:

1. **Backend API Test:**
   - Open http://localhost:8000/docs
   - Try the `/health` endpoint
   - Should return `{"status": "healthy"}`

2. **Frontend Test:**
   - Open http://localhost:3000
   - Search for "WIDGET"
   - Should see AI analysis and results

## Next Steps

### Customize the Analysis

Edit risk scoring weights in `backend/app/services/risk_scorer.py`:

```python
SIMILARITY_WEIGHT = 0.40
CLASS_OVERLAP_WEIGHT = 0.30
STATUS_STRENGTH_WEIGHT = 0.20
USE_COMMERCE_WEIGHT = 0.10
```

### Customize the Design

Edit colors in `frontend/tailwind.config.ts`:

```typescript
risk: {
  critical: '#DC2626',
  high: '#EA580C',
  // ...
}
```

### Add Real USPTO Search

The current implementation uses mock data. To integrate real USPTO search API:

1. Research USPTO's full-text search endpoints
2. Update `backend/app/services/uspto.py`
3. Replace `_mock_search()` with real API calls

## Running in Production

### Backend

```bash
# Install production server
pip install gunicorn

# Run with gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### Frontend

```bash
# Build optimized production bundle
npm run build

# Start production server
npm start
```

## Stopping the Servers

When you're done:

1. **Frontend:** Press `Ctrl+C` in the frontend terminal
2. **Backend:** Press `Ctrl+C` in the backend terminal
3. **Deactivate Python venv:** Run `deactivate`

## Summary of Terminal Commands

**Terminal 1 (Backend):**
```bash
cd /Users/tomsuharto/Documents/Obsidian\ Vault/Claude\ Code/USPTO/backend
source venv/bin/activate
uvicorn app.main:app --reload --port 8000
```

**Terminal 2 (Frontend):**
```bash
cd /Users/tomsuharto/Documents/Obsidian\ Vault/Claude\ Code/USPTO/frontend
npm run dev
```

## Need Help?

- Check the main README.md for architecture details
- Review PROJECT-SPEC.md for feature specifications
- Check backend/README.md for API documentation
- Check frontend/README.md for component details

## Success Checklist

- [✓] Python 3.11+ installed
- [✓] Node.js 18+ installed
- [✓] USPTO API key configured
- [ ] Anthropic API key obtained and configured
- [ ] Backend dependencies installed
- [ ] Frontend dependencies installed
- [ ] Backend running on :8000
- [ ] Frontend running on :3000
- [ ] Successful test search completed

---

Ready to analyze trademarks! 🚀
