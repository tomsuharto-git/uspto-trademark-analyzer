#!/bin/bash

# Automated Railway Deployment Script
# Deploys the latest backend code to Railway

set -e

echo "🚂 Railway Backend Deployment"
echo "==============================="
echo ""

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLI not found. Install it with:"
    echo "   npm install -g @railway/cli"
    exit 1
fi

# Navigate to repository root
cd "$(dirname "$0")"

# Show current commit
echo "📝 Current commit:"
git log -1 --oneline
echo ""

# Verify all changes are committed
if ! git diff-index --quiet HEAD --; then
    echo "⚠️  Warning: You have uncommitted changes"
    read -p "Continue anyway? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Make sure latest is pushed
echo "🔄 Pushing to GitHub..."
git push origin main
echo ""

# Deploy to Railway
echo "🚀 Triggering Railway deployment..."
echo ""
echo "Choose deployment method:"
echo "  1) Redeploy using Railway CLI (requires linked project)"
echo "  2) Manual redeploy (opens Railway dashboard)"
echo ""
read -p "Select (1-2): " -n 1 -r
echo ""

case $REPLY in
    1)
        # Try CLI deployment
        echo "Attempting Railway CLI deployment..."
        railway up
        ;;
    2)
        # Open Railway dashboard
        echo "Opening Railway dashboard..."
        echo ""
        echo "In the dashboard:"
        echo "  1. Find the 'uspto-backend' service"
        echo "  2. Click the '...' menu"
        echo "  3. Select 'Redeploy'"
        echo ""
        open "https://railway.app/project/$(railway environment | grep -oP '(?<=Project: ).*')"
        ;;
    *)
        echo "❌ Invalid selection"
        exit 1
        ;;
esac

echo ""
echo "✅ Deployment triggered!"
echo ""
echo "📊 Monitor deployment:"
echo "   railway logs"
echo ""
echo "🔗 Backend URL:"
echo "   https://uspto-backend-production.up.railway.app/"
