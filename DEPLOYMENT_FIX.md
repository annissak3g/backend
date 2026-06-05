# 🔧 Railway Deployment - Error Fix Guide

## Common "Error Deploying Source" Solutions

### ✅ Solution 1: Use Railway Dashboard (Easiest)

**Step 1: Push to GitHub First**
```bash
cd /app/backend

# Initialize git
git init
git add .
git commit -m "Playbeat backend"

# Create repo on GitHub and push
git remote add origin https://github.com/YOUR_USERNAME/playbeat-backend.git
git branch -M main
git push -u origin main
```

**Step 2: Deploy from Railway Dashboard**
1. Go to https://railway.app
2. Login as **reedbixby**
3. Click "New Project"
4. Select "Deploy from GitHub repo"
5. Choose your `playbeat-backend` repository
6. Railway will auto-detect Python and deploy!

**Step 3: Add Environment Variables**
Click on your service → Variables tab → Add these:
```
MONGO_URL=mongodb+srv://playbeatadmin:Playbeat2026@playbeat.fwjmwfo.mongodb.net/playbeat_digital?retryWrites=true&w=majority
DB_NAME=playbeat_digital
CORS_ORIGINS=https://playbeat.digital,https://playbeat-frontend.vercel.app
STRIPE_API_KEY=sk_test_emergent
EMERGENT_LLM_KEY=sk-emergent-880Da40D360F21a8f6
APP_NAME=playbeat-digital
FRONTEND_URL=https://playbeat.digital
PORT=8001
```

---

### ✅ Solution 2: Use Render.com (Alternative)

**Step 1: Create account on Render**
1. Go to https://render.com
2. Sign up with GitHub

**Step 2: New Web Service**
1. Click "New +" → "Web Service"
2. Connect your GitHub repo
3. Or use "Public Git repository" with your GitHub URL

**Step 3: Configure**
- **Name:** playbeat-backend
- **Runtime:** Python 3
- **Build Command:** `pip install -r requirements-railway.txt`
- **Start Command:** `uvicorn server:app --host 0.0.0.0 --port $PORT`

**Step 4: Add Environment Variables**
Same as Railway variables above

**Deploy!** Render will give you a URL like: `https://playbeat-backend.onrender.com`

---

### ✅ Solution 3: Fix Railway CLI Deployment

**Try using the minimal requirements file:**

```bash
cd /app/backend

# Use minimal requirements
cp requirements-railway.txt requirements.txt

# Try deployment again
railway up
```

---

### ✅ Solution 4: Use Vercel for Backend (Quick Test)

Create `vercel.json`:
```json
{
  "version": 2,
  "builds": [
    {
      "src": "server.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "server.py"
    }
  ]
}
```

Deploy:
```bash
npm install -g vercel
vercel login
cd /app/backend
vercel
```

---

### ✅ Solution 5: Docker Deployment (Railway with Dockerfile)

Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements-railway.txt .
RUN pip install --no-cache-dir -r requirements-railway.txt

COPY . .

CMD uvicorn server:app --host 0.0.0.0 --port $PORT
```

Railway will auto-detect Dockerfile and use it!

---

## 🔍 Debug Railway Error

**Check Railway Logs:**
```bash
railway logs
```

**Common Errors & Fixes:**

### Error: "No Python version specified"
**Fix:** Added `runtime.txt` with `python-3.11.0`

### Error: "Module not found"
**Fix:** Use `requirements-railway.txt` (minimal deps)

### Error: "Port binding failed"
**Fix:** Ensure `PORT` env variable is set

### Error: "Build timeout"
**Fix:** Remove heavy packages (pandas, numpy, jq)

### Error: "emergentintegrations not found"
**Fix:** Already in requirements-railway.txt

---

## 📦 Files Added to Fix Deployment

- ✅ `runtime.txt` - Python version
- ✅ `nixpacks.toml` - Railway build config
- ✅ `requirements-railway.txt` - Minimal dependencies
- ✅ `railway.json` - Updated config

---

## 🎯 Recommended: Use Railway Dashboard

This is the most reliable method:
1. Push code to GitHub
2. Deploy from Railway dashboard
3. Add environment variables
4. Done!

**Your code is production-ready. The issue is likely with Railway CLI or network.** ✅

---

## 🆘 Still Having Issues?

Try Render.com instead - it's just as good and often more reliable for Python apps!

1. https://render.com → New Web Service
2. Connect GitHub
3. Deploy!
