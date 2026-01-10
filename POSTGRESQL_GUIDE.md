# Deploying to Render with PostgreSQL Database

## 🚀 Quick Deploy with Persistent Storage

### Step 1: Create PostgreSQL Database (Free)

1. **Go to [Render Dashboard](https://dashboard.render.com)**
2. Click **"New +"** → **"PostgreSQL"**
3. Configure database:
   - **Name:** `vit-sentiment-db`
   - **Database:** `sentiment_analysis`
   - **User:** `sentiment_user` (auto-generated)
   - **Region:** Choose closest to you
   - **Instance Type:** **Free** (1 GB storage)
4. Click **"Create Database"**
5. Wait 1-2 minutes for database to provision
6. **Copy the "Internal Database URL"** (starts with `postgres://`)

### Step 2: Deploy Web Service

1. **Push your code to GitHub:**
   ```bash
   git add .
   git commit -m "Add PostgreSQL support"
   git push origin main
   ```

2. **Create Web Service:**
   - Go to [Render Dashboard](https://dashboard.render.com)
   - Click **"New +"** → **"Web Service"**
   - Connect your repository: `abhinavamirtharaj-cpu/Vit-science-project-`

3. **Configure Service:**
   - **Name:** `vit-sentiment-analyzer`
   - **Environment:** Python 3
   - **Build Command:** 
     ```
     pip install -r requirements.txt && python -m textblob.download_corpora
     ```
   - **Start Command:** 
     ```
     gunicorn run:app
     ```

4. **Add Environment Variable:**
   - Scroll to **"Environment Variables"**
   - Click **"Add Environment Variable"**
   - **Key:** `DATABASE_URL`
   - **Value:** Paste the Internal Database URL you copied
   - Or click **"Add from Database"** and select your database

5. **Deploy:**
   - Click **"Create Web Service"**
   - Wait 3-5 minutes for deployment
   - Your app will be live with **persistent storage**!

## 📊 What You Get with PostgreSQL

### ✅ Benefits:
- **Persistent Data** - Messages survive restarts
- **Better Performance** - Faster queries on large datasets
- **Scalability** - Handle thousands of messages
- **Concurrent Access** - Multiple users safely
- **Free Tier:** 1 GB storage (thousands of messages)
- **Automatic Backups** - Render handles this

### 🆚 CSV vs PostgreSQL Comparison:

| Feature | CSV (Free) | PostgreSQL (Free) |
|---------|-----------|-------------------|
| Persistent | ❌ Ephemeral | ✅ Permanent |
| Storage | Lost on restart | 1 GB persistent |
| Performance | Slow with >1000 msgs | Fast even with 100k+ |
| Concurrent Users | ⚠️ Race conditions | ✅ Safe |
| Backup | Manual only | Automatic |
| Cost | $0 | $0 |

## 🔧 How It Works

The app **automatically detects** which storage to use:

```python
# If DATABASE_URL is set → Use PostgreSQL
# If DATABASE_URL is empty → Use CSV

# No code changes needed!
```

When you set the `DATABASE_URL` environment variable in Render, the app automatically switches to PostgreSQL. Remove it, and it falls back to CSV.

## 📝 Verify It's Working

After deployment:

1. **Check Logs:**
   - Go to your web service in Render
   - Click "Logs"
   - Look for: `✓ Using PostgreSQL database for storage`

2. **Test the App:**
   - Visit your Render URL
   - Send a few chat messages
   - **Restart your service** (Manual Deploy → Deploy)
   - Visit again - your messages should still be there!

## 🛠️ Local Development with PostgreSQL

### Option 1: Use Render's Database from Local
```bash
# Set environment variable
export DATABASE_URL="your-internal-database-url"

# Run locally
python run.py
```

### Option 2: Use Docker PostgreSQL
```bash
# Start PostgreSQL container
docker run --name postgres-dev -e POSTGRES_PASSWORD=dev123 -p 5432:5432 -d postgres:15

# Set environment variable
export DATABASE_URL="postgresql://postgres:dev123@localhost:5432/sentiment_db"

# Run locally
python run.py
```

### Option 3: Use CSV Locally (Default)
```bash
# Just run without DATABASE_URL
python run.py

# Will use CSV files in models/
```

## 🔍 Database Management

### View Data in Render Dashboard:
1. Go to your PostgreSQL database in Render
2. Click "Connect" → Get connection string
3. Use any PostgreSQL client:
   - **pgAdmin** (GUI)
   - **DBeaver** (GUI)
   - **psql** (CLI)

### Query Examples:
```sql
-- View all messages
SELECT * FROM chat_messages ORDER BY saved_at DESC LIMIT 50;

-- Count messages by sentiment
SELECT sentiment_category, COUNT(*) 
FROM chat_messages 
GROUP BY sentiment_category;

-- Get messages from specific contact
SELECT text, sentiment_emoji, saved_at 
FROM chat_messages 
WHERE contact_id = 'user123'
ORDER BY saved_at DESC;
```

## 💰 Cost & Limits

### Free Tier (PostgreSQL):
- **Storage:** 1 GB
- **Rows:** ~100,000 messages (with typical data)
- **Backups:** Automatic (7 days)
- **Expires:** 90 days if no activity (free tier only)

### Need More?
**Starter Plan:** $7/month
- 10 GB storage
- ~1 million messages
- Never expires
- Better performance

## 🐛 Troubleshooting

### "Database connection failed"
- Verify `DATABASE_URL` is set correctly in Render dashboard
- Check database is running (not suspended)
- Ensure using "Internal Database URL" (not External)

### "Module 'psycopg2' not found"
- Check `requirements.txt` includes `psycopg2-binary`
- Rebuild your web service

### App uses CSV instead of PostgreSQL
- Check environment variable is set
- Look for logs: `✓ Using PostgreSQL` vs `✓ Using CSV`
- Restart the service after adding DATABASE_URL

### Old CSV data not in database
- Data migration needed (see below)

## 📤 Migrate CSV Data to PostgreSQL

If you have existing CSV data:

1. **Export your CSV:**
   ```bash
   # Download from Render or use local copy
   cp models/chat_history_global.csv backup.csv
   ```

2. **Create migration script** (create `migrate_csv_to_db.py`):
   ```python
   import csv
   import os
   os.environ['DATABASE_URL'] = 'your-database-url'
   
   from ui_io.database import init_db, ChatMessage, get_session
   from datetime import datetime
   
   init_db()
   session = get_session()
   
   with open('backup.csv', 'r') as f:
       reader = csv.DictReader(f)
       for row in reader:
           msg = ChatMessage(
               contact_id=row['contact_id'],
               contact_name=row['contact_name'],
               direction=row['dir'],
               text=row['text'],
               sentiment_category=row['sentiment_category'],
               # ... add other fields
           )
           session.add(msg)
   
   session.commit()
   print("Migration complete!")
   ```

3. **Run migration:**
   ```bash
   python migrate_csv_to_db.py
   ```

## 🎯 Recommended Setup

**For Development:** Use CSV (simple, no setup)
**For Production:** Use PostgreSQL (reliable, persistent)

Your code automatically handles both! 🎉

## 📚 Additional Resources

- [Render PostgreSQL Docs](https://render.com/docs/databases)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [PostgreSQL Best Practices](https://render.com/docs/postgresql-best-practices)
