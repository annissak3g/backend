# 🚂 Railway Deployment Guide for Playbeat Digital Backend

## Account Details
- **Email:** playbeatdigital@gmail.com
- **Username:** playbeatdigital-tech

---

## 🚀 Method 1: Deploy via Railway Dashboard (Easiest)

### Step 1: Login to Railway
1. Go to https://railway.app
2. Click "Login" 
3. Sign in with GitHub or use email: playbeatdigital@gmail.com

### Step 2: Create New Project
1. Click "New Project"
2. Select "Deploy from GitHub repo"
3. Connect your GitHub account if not already connected
4. Select your backend repository

**OR if you don't have a GitHub repo yet:**
1. Click "Empty Project"
2. We'll push code via Railway CLI (see Method 2)

### Step 3: Configure Environment Variables
Once project is created, click on your service → "Variables" tab

Add these variables:

```
MONGO_URL=mongodb+srv://playbeatadmin:Playbeat2026@playbeat.fwjmwfo.mongodb.net/playbeat_digital?retryWrites=true&w=majority
DB_NAME=playbeat_digital
CORS_ORIGINS=https://playbeat.digital,https://playbeat-frontend.vercel.app,https://*.vercel.app
STRIPE_API_KEY=sk_test_emergent
EMERGENT_LLM_KEY=sk-emergent-880Da40D360F21a8f6
APP_NAME=playbeat-digital
FRONTEND_URL=https://playbeat.digital
PORT=8001
```

### Step 4: Configure Start Command
In "Settings" → "Deploy":
- **Start Command:** `uvicorn server:app --host 0.0.0.0 --port $PORT`
- **Root Directory:** `/backend` (if backend is in a subfolder)

### Step 5: Deploy
- Railway will automatically detect Python and install requirements.txt
- Wait for deployment to complete (2-3 minutes)
- Railway will provide a URL like: `https://playbeat-backend-production.up.railway.app`

### Step 6: Test Your Deployment
```bash
curl https://your-railway-url.up.railway.app/api/products
```

You should see your 8 products returned!

---

## 🚀 Method 2: Deploy via Railway CLI (Alternative)

### Step 1: Install Railway CLI
```bash
npm install -g @railway/cli
```

### Step 2: Login
```bash
railway login
```
This will open browser - login with: playbeatdigital@gmail.com

### Step 3: Initialize Project
```bash
cd /app/backend
railway init
```
- Choose "Create new project"
- Name it: "playbeat-backend" or "playbeat-api"

### Step 4: Link and Deploy
```bash
railway link
railway up
```

### Step 5: Add Environment Variables
```bash
railway variables set MONGO_URL="mongodb+srv://playbeatadmin:Playbeat2026@playbeat.fwjmwfo.mongodb.net/playbeat_digital?retryWrites=true&w=majority"
railway variables set DB_NAME="playbeat_digital"
railway variables set CORS_ORIGINS="https://playbeat.digital,https://playbeat-frontend.vercel.app"
railway variables set STRIPE_API_KEY="sk_test_emergent"
railway variables set EMERGENT_LLM_KEY="sk-emergent-880Da40D360F21a8f6"
railway variables set APP_NAME="playbeat-digital"
railway variables set FRONTEND_URL="https://playbeat.digital"
railway variables set PORT="8001"
```

### Step 6: Get Your URL
```bash
railway domain
```

---

## 📝 After Deployment

### 1. Update BACKEND_URL Environment Variable
Once you have your Railway URL, update it:

**In Railway Dashboard:**
- Add variable: `BACKEND_URL=https://your-actual-railway-url.up.railway.app`

**OR via CLI:**
```bash
railway variables set BACKEND_URL="https://your-actual-railway-url.up.railway.app"
```

### 2. Update Frontend in Vercel

Go to: https://vercel.com/playbeat/playbeat-frontend

**Settings → Environment Variables:**

Add or update:
```
REACT_APP_API_URL=https://your-railway-url.up.railway.app/api
```
OR
```
VITE_API_URL=https://your-railway-url.up.railway.app/api
```

Then click "Redeploy"

### 3. Test Full Integration

**Test Products API:**
```bash
curl https://your-railway-url.up.railway.app/api/products
```

**Test from Frontend:**
Visit https://playbeat.digital and check if products load!

---

## 🔍 Monitoring & Logs

### View Logs
**Via Dashboard:**
- Railway Dashboard → Your Project → "Deployments" → Click latest deployment

**Via CLI:**
```bash
railway logs
```

### Check Status
```bash
railway status
```

---

## ⚠️ Troubleshooting

### Error: "Application failed to respond"
- Check Railway logs
- Verify PORT environment variable is set
- Ensure start command is correct: `uvicorn server:app --host 0.0.0.0 --port $PORT`

### Error: "CORS error"
- Verify CORS_ORIGINS includes your frontend URL
- Restart Railway service after adding env vars

### Error: "MongoDB connection failed"
- Check MongoDB Atlas allows connections from 0.0.0.0/0
- Verify MONGO_URL is correct

### Products not loading
- Run seed script: `railway run python seed_products.py`

---

## 🎯 Quick Deploy Checklist

- [ ] Railway account created/logged in
- [ ] New project created
- [ ] All environment variables added
- [ ] Backend deployed successfully
- [ ] Railway URL obtained
- [ ] Backend URL tested (curl /api/products)
- [ ] BACKEND_URL env variable updated in Railway
- [ ] Frontend REACT_APP_API_URL updated in Vercel
- [ ] Frontend redeployed
- [ ] Full flow tested on https://playbeat.digital

---

## 📞 Support

If you encounter issues:
1. Check Railway logs: `railway logs`
2. Check Railway status: https://railway.app/status
3. Verify all environment variables are set correctly

**Your backend is production-ready! 🚀**
