#!/bin/bash

echo "🚂 Playbeat Digital - Railway Deployment"
echo "========================================="
echo "Railway Username: reedbixby"
echo "Email: playbeatdigital@gmail.com"
echo ""

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "📦 Installing Railway CLI..."
    npm install -g @railway/cli
    echo ""
else
    echo "✅ Railway CLI already installed"
    echo ""
fi

echo "🔐 Step 1: Login to Railway"
echo "   Use account: reedbixby (playbeatdigital@gmail.com)"
echo ""
read -p "Press Enter to login..."
railway login

echo ""
echo "🏗️  Step 2: Initialize Railway project"
echo "   Project name suggestion: playbeat-backend"
echo ""
railway init

echo ""
echo "🚀 Step 3: Deploying to Railway..."
railway up

echo ""
echo "⚙️  Step 4: Setting environment variables..."
echo ""

railway variables set MONGO_URL="mongodb+srv://playbeatadmin:Playbeat2026@playbeat.fwjmwfo.mongodb.net/playbeat_digital?retryWrites=true&w=majority"
railway variables set DB_NAME="playbeat_digital"
railway variables set CORS_ORIGINS="https://playbeat.digital,https://playbeat-frontend.vercel.app,https://*.vercel.app"
railway variables set STRIPE_API_KEY="sk_test_emergent"
railway variables set EMERGENT_LLM_KEY="sk-emergent-880Da40D360F21a8f6"
railway variables set APP_NAME="playbeat-digital"
railway variables set FRONTEND_URL="https://playbeat.digital"
railway variables set PORT="8001"

echo ""
echo "🌐 Step 5: Getting your Railway URL..."
RAILWAY_URL=$(railway domain 2>&1 | grep -o 'https://[^"]*' | head -1)

if [ -z "$RAILWAY_URL" ]; then
    echo "⚠️  Could not auto-detect URL. Run manually:"
    echo "   railway domain"
else
    echo "✅ Your Railway URL: $RAILWAY_URL"
fi

echo ""
echo "📝 Setting BACKEND_URL environment variable..."
if [ ! -z "$RAILWAY_URL" ]; then
    railway variables set BACKEND_URL="$RAILWAY_URL"
fi

echo ""
echo "=============================================="
echo "✅ DEPLOYMENT COMPLETE!"
echo "=============================================="
echo ""
echo "🔗 Your Backend URLs:"
echo "   Railway Project: https://railway.app/project"
echo "   API Endpoint: $RAILWAY_URL/api"
echo ""
echo "🧪 Test your API:"
if [ ! -z "$RAILWAY_URL" ]; then
    echo "   curl $RAILWAY_URL/api/products"
else
    echo "   railway domain  # Get your URL first"
    echo "   curl <your-url>/api/products"
fi
echo ""
echo "📝 NEXT STEPS:"
echo "   1. Copy your Railway URL above"
echo "   2. Go to: https://vercel.com/playbeat/playbeat-frontend"
echo "   3. Settings → Environment Variables"
echo "   4. Add: REACT_APP_API_URL = <your-railway-url>/api"
echo "   5. Click 'Redeploy'"
echo ""
echo "🎉 Your backend is live!"
