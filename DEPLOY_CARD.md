# 🎯 Playbeat Digital - Quick Deploy Card

## Your Account Details
- **Railway Username:** reedbixby
- **Email:** playbeatdigital@gmail.com
- **Frontend:** https://playbeat.digital (Vercel)
- **Database:** MongoDB Atlas (already connected & populated)

---

## 🚀 ONE COMMAND DEPLOY

```bash
cd backend
./deploy-railway.sh
```

**This will:**
1. ✅ Login to Railway (username: reedbixby)
2. ✅ Create new project
3. ✅ Deploy your backend
4. ✅ Set all environment variables
5. ✅ Give you your backend URL

**Time: ~5 minutes**

---

## 📋 Manual Deploy (Alternative)

```bash
# 1. Install Railway CLI
npm install -g @railway/cli

# 2. Login (username: reedbixby)
railway login

# 3. Deploy
cd backend
railway init
railway up

# 4. Set environment variables (copy all)
railway variables set MONGO_URL="mongodb+srv://playbeatadmin:Playbeat2026@playbeat.fwjmwfo.mongodb.net/playbeat_digital?retryWrites=true&w=majority"
railway variables set DB_NAME="playbeat_digital"
railway variables set CORS_ORIGINS="https://playbeat.digital,https://playbeat-frontend.vercel.app"
railway variables set STRIPE_API_KEY="sk_test_emergent"
railway variables set EMERGENT_LLM_KEY="sk-emergent-880Da40D360F21a8f6"
railway variables set APP_NAME="playbeat-digital"
railway variables set FRONTEND_URL="https://playbeat.digital"
railway variables set PORT="8001"

# 5. Get your URL
railway domain
```

---

## 🔗 After Deployment

### Connect Frontend to Backend:

1. **Get Railway URL** from deployment (e.g., `https://playbeat-backend.up.railway.app`)

2. **Update Vercel:**
   - Go to: https://vercel.com/playbeat/playbeat-frontend/settings/environment-variables
   - Add new variable:
     ```
     Name: REACT_APP_API_URL
     Value: https://your-railway-url.up.railway.app/api
     ```
   - Save and Redeploy

3. **Test Everything:**
   ```bash
   # Test backend
   curl https://your-railway-url.up.railway.app/api/products
   
   # Should return 8 products!
   ```

4. **Visit your website:**
   - https://playbeat.digital
   - Products should load!

---

## 📊 MongoDB Atlas Access

**Already set up with 8 products!**

**Access from your PC:**

1. **MongoDB Compass (Recommended):**
   - Download: https://www.mongodb.com/try/download/compass
   - Connection string:
     ```
     mongodb+srv://playbeatadmin:Playbeat2026@playbeat.fwjmwfo.mongodb.net/playbeat_digital
     ```

2. **MongoDB Atlas Dashboard:**
   - URL: https://cloud.mongodb.com
   - Login: playbeatdigital@gmail.com

---

## ✅ Verification Checklist

- [ ] Railway CLI installed
- [ ] Logged in as reedbixby
- [ ] Backend deployed to Railway
- [ ] Environment variables set
- [ ] Railway URL obtained
- [ ] BACKEND_URL set in Railway
- [ ] REACT_APP_API_URL set in Vercel
- [ ] Frontend redeployed
- [ ] Backend API tested (`curl /api/products`)
- [ ] Frontend tested (visit https://playbeat.digital)

---

## 🆘 Quick Troubleshooting

**"railway: command not found"**
```bash
npm install -g @railway/cli
```

**Can't login?**
- Use username: reedbixby
- Use email: playbeatdigital@gmail.com

**Deployment failed?**
```bash
railway logs  # Check error logs
```

**CORS error on frontend?**
- Verify CORS_ORIGINS includes https://playbeat.digital
- Restart Railway service

**Products not loading?**
```bash
railway run python seed_products.py
```

---

## 📞 Support Links

- **Railway Dashboard:** https://railway.app/dashboard
- **Railway Docs:** https://docs.railway.app
- **MongoDB Atlas:** https://cloud.mongodb.com
- **Vercel Dashboard:** https://vercel.com/dashboard

---

## 🎉 You're Ready!

**Everything is configured:**
- ✅ Backend code ready
- ✅ MongoDB Atlas populated (8 products)
- ✅ Stripe payments configured
- ✅ Deploy script ready
- ✅ Documentation complete

**Just run:**
```bash
./deploy-railway.sh
```

**Then update Vercel and you're LIVE! 🚀**
