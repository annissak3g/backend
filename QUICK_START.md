# 🎯 DEPLOYMENT READY - Quick Start Guide

## Your Setup
- **Account:** playbeatdigital@gmail.com
- **Frontend:** https://playbeat.digital (Vercel)
- **Backend:** Ready to deploy to Railway

---

## 🚀 FASTEST WAY - One Command Deploy

```bash
cd /app/backend
./deploy-railway.sh
```

This script will:
1. ✅ Install Railway CLI (if needed)
2. ✅ Login to Railway
3. ✅ Create new project
4. ✅ Deploy your code
5. ✅ Set all environment variables
6. ✅ Give you your backend URL

**Time: ~5 minutes**

---

## 📋 OR Manual Steps (if you prefer)

### Step 1: Login to Railway
```bash
npm install -g @railway/cli
railway login
```
Use: playbeatdigital@gmail.com

### Step 2: Deploy
```bash
cd /app/backend
railway init
railway up
```

### Step 3: Add Environment Variables
Copy-paste this block:
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

### Step 4: Get Your URL
```bash
railway domain
```

---

## 🔗 Connect Frontend to Backend

### In Vercel (https://vercel.com/playbeat/playbeat-frontend):

1. Go to **Settings → Environment Variables**
2. Add new variable:
   ```
   Name: REACT_APP_API_URL
   Value: https://your-railway-url.up.railway.app/api
   ```
3. Click **Save**
4. Go to **Deployments** → Click **"..."** → **Redeploy**

---

## ✅ Verification

### Test Backend:
```bash
curl https://your-railway-url.up.railway.app/api/products
```

Should return 8 products!

### Test Frontend:
1. Visit https://playbeat.digital
2. Products should load on the page
3. Add to cart should work
4. Checkout should work with Stripe

---

## 📊 What You Have

**Backend Features:**
- ✅ 8 Products seeded (IPTV, Netflix, Spotify, Office, Windows, Gift Cards)
- ✅ Shopping cart functionality
- ✅ Stripe payment integration
- ✅ Order management
- ✅ Admin dashboard with Google OAuth
- ✅ Customer management
- ✅ MongoDB Atlas connected
- ✅ All APIs tested and working

**API Endpoints:**
- Public: Products, Cart, Checkout, Orders
- Admin: Dashboard stats, Customers, Orders management

---

## 🆘 Need Help?

**Common Issues:**

1. **"railway: command not found"**
   ```bash
   npm install -g @railway/cli
   ```

2. **CORS error on frontend**
   - Verify CORS_ORIGINS includes https://playbeat.digital
   - Restart Railway service

3. **Products not showing**
   - Run: `railway run python seed_products.py`

**Check Logs:**
```bash
railway logs
```

---

## 🎉 You're All Set!

Your backend is production-ready with:
- FastAPI + MongoDB Atlas
- Stripe payments
- Google OAuth admin access
- Complete REST API
- Deployment scripts

**Deploy now with:** `cd /app/backend && ./deploy-railway.sh`

---

**Next:** After deployment, your https://playbeat.digital will be fully functional! 🚀
