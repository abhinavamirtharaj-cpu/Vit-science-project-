# 100% Free Deployment to Render (No Credit Card Required)

## ✅ Free Tier Deploy - 2 Easy Steps

### Step 1: Deploy Web App (Free - No Payment)

1. **Go to [Render Dashboard](https://dashboard.render.com)**
2. Click **"New +"** → **"Web Service"**
3. Click **"Build and deploy from a Git repository"** → **Next**
4. Connect to your GitHub: `abhinavamirtharaj-cpu/Vit-science-project-`
5. Configure:
   - **Name:** `vit-sentiment-analyzer` (or any name)
   - **Branch:** `clone`
   - **Root Directory:** Leave blank
   - **Environment:** `Python 3`
   - **Build Command:** 
     ```
     pip install -r requirements.txt && python -m textblob.download_corpora
     ```
   - **Start Command:** 
     ```
     gunicorn run:app
     ```
   - **Instance Type:** **Free**

6. Click **"Create Web Service"**
7. Wait 3-5 minutes - Your app will be live!

**✅ Your app is now running with CSV storage (works perfectly for testing)**

### Step 2: Add PostgreSQL Database (Optional - Also Free)

If you want persistent storage:

1. **In Render Dashboard** → Click **"New +"** → **"PostgreSQL"**
2. Configure:
   - **Name:** `vit-sentiment-db`
   - **Database:** `sentiment_analysis`
   - **Region:** Choose closest to your web service
   - **Instance Type:** **Free**
3. Click **"Create Database"**
4. Wait 1-2 minutes for provisioning
5. Go to your database → Copy **"Internal Database URL"**

6. **Connect to Web Service:**
   - Go back to your web service
   - Click **"Environment"** tab
   - Click **"Add Environment Variable"**
   - Key: `DATABASE_URL`
   - Value: Paste the Internal Database URL
   - Click **"Save Changes"**

7. Your service will auto-restart and use PostgreSQL!

## 💰 Cost Breakdown

| Resource | Free Tier | Your Cost |
|----------|-----------|-----------|
| Web Service | 750 hours/month | **$0** |
| PostgreSQL | 1 GB storage | **$0** |
| Data Transfer | 100 GB/month | **$0** |
| **Total** | | **$0** |

## ⚠️ Free Tier Limitations

**Web Service:**
- Sleeps after 15 min of inactivity
- First request after sleep: ~30 seconds wake time
- 512 MB RAM

**PostgreSQL (if added):**
- 1 GB storage (~100,000 messages)
- Expires after 90 days of no connections
- Limited connections (10 max)

## 🎯 What Works on Free Tier

✅ Full sentiment analysis  
✅ Chat interface  
✅ Color-coded messages  
✅ Real-time analysis  
✅ CSV storage (immediate)  
✅ PostgreSQL storage (if you add it)  
✅ HTTPS enabled automatically  
✅ Custom domain support  

## 🚀 Alternative: Deploy Without Database

**Simplest Option - Just Web Service:**
- Uses CSV files (works great for testing)
- No database setup needed
- Still 100% free
- Data resets on service restart (not ideal for production)

**To deploy this way:** Just do Step 1 above, skip Step 2!

## 📱 Access Your App

After deployment:
- Your URL: `https://vit-sentiment-analyzer.onrender.com`
- Click "Chat Here" button
- Send messages and see sentiment analysis!

## 🐛 Troubleshooting

**"Payment method required"**
- Use the manual steps above instead of Blueprint
- Blueprint might require payment verification
- Manual deployment is 100% free, no card needed

**App is slow or times out on first visit**
- Free tier sleeps after 15 min inactivity
- First request wakes it up (~30 sec)
- Subsequent requests are fast

**"Build failed"**
- Check Build Logs in Render dashboard
- Verify `requirements.txt` exists
- Ensure branch is set to `clone`

**Database connection failed**
- Verify DATABASE_URL is set correctly
- Use "Internal Database URL" not External
- Check database is running (not expired)

## 💡 Tips

1. **Keep app awake:** Use a service like [UptimeRobot](https://uptimerobot.com) (also free) to ping your app every 5 minutes
2. **Local testing:** Run `python run.py` locally before deploying
3. **Check logs:** Render dashboard → Logs tab to see any errors
4. **Deploy updates:** Just push to GitHub - Render auto-deploys!

## 🎉 Success!

Your sentiment analysis app is now live on Render's free tier, no credit card required!
