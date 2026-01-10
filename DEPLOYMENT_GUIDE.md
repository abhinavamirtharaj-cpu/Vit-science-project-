# Deploying to Render

## Quick Deploy Steps

### Option 1: Deploy via GitHub (Recommended)

1. **Push your code to GitHub:**
   ```bash
   git add .
   git commit -m "Prepare for Render deployment"
   git push origin main
   ```

2. **Connect to Render:**
   - Go to [render.com](https://render.com)
   - Sign up or log in
   - Click "New +" → "Web Service"
   - Connect your GitHub repository: `abhinavamirtharaj-cpu/Vit-science-project-`

3. **Configure the service:**
   - **Name:** `vit-sentiment-analyzer` (or any name you prefer)
   - **Environment:** Python 3
   - **Build Command:** `pip install -r requirements.txt && python -m textblob.download_corpora`
   - **Start Command:** `gunicorn run:app`
   - **Instance Type:** Free tier is fine for testing

4. **Deploy:**
   - Click "Create Web Service"
   - Wait 3-5 minutes for deployment
   - Your app will be live at: `https://vit-sentiment-analyzer.onrender.com`

### Option 2: Deploy via Blueprint (render.yaml)

1. **Push your code to GitHub** (with the `render.yaml` file)

2. **Deploy via Blueprint:**
   - Go to [render.com](https://render.com)
   - Click "New +" → "Blueprint"
   - Connect your repository
   - Render will automatically detect and use `render.yaml`

### Option 3: Manual Configuration

If you prefer manual setup:
- **Runtime:** Python 3.12.1
- **Build Command:** `pip install -r requirements.txt && python -m textblob.download_corpora`
- **Start Command:** `gunicorn run:app`

## Important Notes

### ✅ What's Included:
- Flask web server with gunicorn (production-ready)
- TextBlob NLP sentiment analysis
- Automatic corpus download during build
- CSV data persistence
- All core features working

### ⚠️ Limitations on Free Tier:
- **File Storage:** CSV files are ephemeral on Render free tier
  - Files are stored but reset on service restarts
  - Consider upgrading to paid tier or using external database for persistent storage
- **Sleep Mode:** Free services sleep after 15 minutes of inactivity
  - First request after sleep takes ~30 seconds to wake up
- **Build Time:** ~2-3 minutes (downloading NLTK corpora)

### 🔄 Auto-Deploy:
Once connected to GitHub, Render automatically deploys on every push to main branch.

## Environment Variables (Optional)

You can set these in Render dashboard:
- `FLASK_ENV=production` (recommended for production)
- `PORT=10000` (Render sets this automatically)

## Testing Your Deployment

After deployment completes:
1. Visit your Render URL (e.g., `https://vit-sentiment-analyzer.onrender.com`)
2. Click "Chat Here" button
3. Send a message to test sentiment analysis
4. Check the colored output (green/yellow/red)

## Troubleshooting

### Build Fails:
- Check that `requirements.txt` is in root directory
- Verify Python version compatibility

### App Doesn't Start:
- Check logs in Render dashboard
- Ensure `gunicorn` is in requirements.txt
- Verify `run.py` imports work correctly

### Sentiment Analysis Not Working:
- Verify NLTK corpora downloaded during build
- Check build logs for download errors

## Upgrading for Production

For serious production use, consider:

1. **Database instead of CSV:**
   ```python
   # Use PostgreSQL (Render provides free instance)
   pip install psycopg2-binary sqlalchemy
   ```

2. **Persistent Storage:**
   - Upgrade to paid Render plan with persistent disk
   - Or use external storage (S3, Cloud Storage)

3. **Performance:**
   - Add Redis for caching
   - Use Render's autoscaling

## Cost

- **Free Tier:** $0/month
  - 750 hours/month free
  - Sleeps after inactivity
  - Ephemeral storage
  
- **Starter Plan:** $7/month
  - Always on
  - More resources
  - Still ephemeral storage

- **Standard Plan:** $25/month
  - Persistent disk available
  - Production-ready

## Support

If you encounter issues:
- Check Render's [documentation](https://render.com/docs)
- Review deployment logs in Render dashboard
- Check this project's GitHub issues
