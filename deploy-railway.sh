#!/bin/bash

# Railway Deployment Helper Script
# This script guides you through deploying the USPTO backend to Railway

set -e

echo "🚂 USPTO Trademark Analyzer - Railway Deployment"
echo "=================================================="
echo ""

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLI not found!"
    echo "Install with: npm i -g @railway/cli"
    exit 1
fi

echo "✅ Railway CLI installed ($(railway --version))"
echo ""

# Check login status
if ! railway whoami &> /dev/null; then
    echo "🔐 You need to login to Railway first"
    echo "Run: railway login"
    echo ""
    echo "After logging in, run this script again."
    exit 1
fi

echo "✅ Logged in to Railway as: $(railway whoami)"
echo ""

# Navigate to backend directory
cd "$(dirname "$0")/backend"
echo "📂 Changed to backend directory"
echo ""

# Initialize or link project
echo "🔗 Step 1: Initialize Railway Project"
echo "--------------------------------------"
echo "Choose a name for your project (e.g., uspto-backend)"
railway init

echo ""
echo "✅ Railway project initialized"
echo ""

# Set environment variables
echo "🔑 Step 2: Setting Environment Variables"
echo "-----------------------------------------"

# Get Anthropic API key from .env file
if [ -f ".env" ]; then
    ANTHROPIC_KEY=$(grep ANTHROPIC_API_KEY .env | cut -d '=' -f2)
    if [ -n "$ANTHROPIC_KEY" ]; then
        echo "Setting ANTHROPIC_API_KEY..."
        railway variables set ANTHROPIC_API_KEY="$ANTHROPIC_KEY"
    fi
fi

echo "Setting USPTO_API_KEY..."
railway variables set USPTO_API_KEY=szbcdzcfpygkhqpzigiuoqapzfgiay

echo "Setting ENVIRONMENT..."
railway variables set ENVIRONMENT=production

echo "Setting DEBUG..."
railway variables set DEBUG=false

echo "Setting CORS_ORIGINS..."
railway variables set CORS_ORIGINS=https://frontend-i6hvfo09t-tomsuharto-3884s-projects.vercel.app

echo ""
echo "✅ Environment variables set"
echo ""

# Deploy
echo "🚀 Step 3: Deploying to Railway"
echo "--------------------------------"
railway up

echo ""
echo "✅ Deployment initiated!"
echo ""

# Get domain
echo "🌐 Step 4: Getting Your Backend URL"
echo "------------------------------------"
sleep 5  # Wait for deployment to start
BACKEND_URL=$(railway domain 2>/dev/null || echo "")

if [ -n "$BACKEND_URL" ]; then
    echo "✅ Backend URL: https://$BACKEND_URL"
    echo ""
    echo "📋 Next Steps:"
    echo "-------------"
    echo "1. Test your backend:"
    echo "   https://$BACKEND_URL/docs"
    echo ""
    echo "2. Update frontend environment variable:"
    echo "   cd ../frontend"
    echo "   vercel env add NEXT_PUBLIC_API_URL production"
    echo "   Enter: https://$BACKEND_URL/api/v1"
    echo ""
    echo "3. Redeploy frontend:"
    echo "   vercel --prod"
    echo ""
else
    echo "⏳ Deployment in progress..."
    echo "Run 'railway domain' in the backend directory to get your URL"
    echo ""
fi

echo "🎉 Railway deployment complete!"
echo ""
echo "View logs: railway logs --follow"
echo "Open dashboard: railway open"
