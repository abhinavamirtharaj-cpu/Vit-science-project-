# Sentiment Analysis - Quick Reference Card

## 🚀 Setup in 3 Steps

```bash
# 1. Install dependencies
pip install -r requirements.txt
python -m textblob.download_corpora

# 2. Run the server
python UI.py

# 3. Open browser
http://127.0.0.1:5000/
```

## 🎨 Sentiment Colors at a Glance

| Sentiment | Emoji | Color | Polarity | Example |
|-----------|-------|-------|----------|---------|
| Very Positive | 😄 | 🟢 #4CAF50 | > 0.3 | "I absolutely love this!" |
| Positive | 🙂 | 🟢 #4CAF50 | 0.1-0.3 | "That's great!" |
| Neutral | 😐 | 🟡 #FFC107 | -0.1-0.1 | "It's okay." |
| Negative | ☹️ | 🔴 #F44336 | -0.3--0.1 | "I don't like it." |
| Very Negative | 😠 | 🔴 #F44336 | < -0.3 | "I hate this!" |

## 📁 Key Files

| File | What It Does |
|------|-------------|
| `sentiment_analyzer.py` | Brain 🧠 - Analyzes emotion |
| `chat_service.py` | Coordinator 🔗 - Glues everything together |
| `storage.py` | Memory 💾 - Saves to CSV |
| `UI.py` | Server 🖥️ - Runs the web app |
| `script.js` | Frontend 🎭 - Shows colored messages |
| `styles.css` | Makeup 💄 - Makes it look pretty |

## 🔌 API Endpoints

### Analyze a Message
```javascript
POST /api/analyze
Content-Type: application/json

{
  "text": "I love this!",
  "contact_id": "user123",
  "contact_name": "John"
}

Response:
{
  "success": true,
  "sentiment": {
    "emoji": "😄",
    "category": "Very Positive",
    "color": "#4CAF50",
    "polarity": 0.825
  }
}
```

### Get Chat History
```
GET /api/history/user123

Response:
{
  "success": true,
  "messages": [...]
}
```

### Health Check
```
GET /api/health

Response:
{
  "status": "ok"
}
```

## 💾 CSV Storage Structure

Messages saved as:
```
contact_id | contact_name | dir | date | time | text | sentiment_polarity | sentiment_category | emoji | color
support    | Support      | sent | 2024-01-15 | 10:30 | I love this! | 0.825 | Very Positive | 😄 | #4CAF50
```

## 🐍 Python Usage

### Direct Analysis
```python
from sentiment_analyzer import analyze_chat_message

result = analyze_chat_message("I love this!")
print(result['emoji'])          # 😄
print(result['category'])       # Very Positive
print(result['color'])          # #4CAF50
print(result['polarity_score']) # 0.825
```

### With Chat Service
```python
from chat_service import process_user_message

contact = {'id': 'user1', 'name': 'John'}
result = process_user_message("I love this!", contact)
# Message analyzed, stored to CSV, and formatted for display
```

### Batch Analysis
```python
from sentiment_analyzer import batch_analyze_messages

messages = ["Great!", "Terrible.", "It's okay."]
results = batch_analyze_messages(messages)
# Returns list of analysis dicts
```

## 🎯 Message Workflow

```
User types → Presses Enter → Frontend calls /api/analyze
    ↓
Backend analyzes with TextBlob → Returns sentiment data
    ↓
Message stored to CSV with sentiment → Response sent to frontend
    ↓
Frontend displays message with color and emoji → Done!
    ↓
User hovers over message → Sees mood description in tooltip
```

## 📊 Data Model

### Message Object
```javascript
{
  text: "I love this!",
  time: "10:30",
  date: "2024-01-15",
  iso: "2024-01-15T10:30:00",
  dir: "sent",
  sentiment: {
    emoji: "😄",
    category: "Very Positive",
    description: "Expressing great joy...",
    color: "#4CAF50",
    polarity: 0.825
  }
}
```

## 🧪 Test Messages

```
Test these to see sentiment analysis in action:

"I love this!"                  → Very Positive 😄
"This is great!"                → Positive 🙂
"It works."                     → Neutral 😐
"I don't like this."            → Negative ☹️
"I hate this so much!"          → Very Negative 😠
```

## ❌ Common Issues & Fixes

| Issue | Fix |
|-------|-----|
| `ModuleNotFoundError: textblob` | `pip install textblob` |
| Messages not colored | Restart Flask with `python UI.py` |
| CSV file not updating | Check Flask is running and has write permissions |
| API returning error | Check browser DevTools (F12) Console for details |

## 📚 Documentation Quick Links

- **QUICK_START.md** - Getting started (5 min read)
- **SENTIMENT_ANALYSIS_GUIDE.md** - Full docs (15 min read)
- **ARCHITECTURE.md** - System design (10 min read)
- **example_usage.py** - Code examples (run it!)

## 🔧 Customization Quick Tips

### Change Sentiment Thresholds
Edit `sentiment_analyzer.py`, function `get_sentiment_category()`:
```python
if polarity > 0.5:  # Make stricter
    return { ... "Very Positive" ... }
```

### Change Colors
Edit `sentiment_analyzer.py`, function `get_sentiment_color()`:
```python
return "#FF0000"  # Your hex color
```

### Add Custom Sentiments
Edit `get_sentiment_category()` with new emoji/description combos.

### Style Messages
Edit `styles.css` sentiment bubble section.

## ⚡ Performance

- Analysis: ~100-200ms per message
- Storage: ~10-20ms per message
- UI Update: ~10-20ms per message
- Total: ~120-240ms (feels instant to user)

## 📋 Checklist

- [ ] Installed dependencies: `pip install -r requirements.txt`
- [ ] Downloaded TextBlob data: `python -m textblob.download_corpora`
- [ ] Started server: `python UI.py`
- [ ] Opened browser: `http://127.0.0.1:5000/`
- [ ] Sent test message
- [ ] Saw colored message with emoji
- [ ] Hovered to see description
- [ ] Checked CSV file: `cat chat_history_global.csv`
- [ ] Ready to customize! 🎉

## 🌟 Feature Highlights

✨ Real-time sentiment analysis  
✨ Color-coded messages (green/red/yellow)  
✨ Emoji sentiment badges  
✨ Hover tooltips with mood descriptions  
✨ Automatic CSV storage  
✨ Trend detection (improving/declining/stable)  
✨ Works offline (CSV local storage)  
✨ Graceful error handling  
✨ Beautiful, modern UI  

## 🚀 You're Ready!

Your sentiment analysis chat is ready to use. Start by:
1. Running `python UI.py`
2. Opening http://127.0.0.1:5000/
3. Sending messages and watching them get colored!

**Happy chatting!** 🎉💬✨

---

For detailed information, check the documentation files:
- QUICK_START.md
- SENTIMENT_ANALYSIS_GUIDE.md
- ARCHITECTURE.md
- example_usage.py
