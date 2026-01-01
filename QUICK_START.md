# Quick Start Guide - Sentiment Analysis Chat

## One-Minute Setup

### 1. Install Dependencies
```bash
pip install flask textblob
python -m textblob.download_corpora
```

### 2. Run the Application
```bash
python UI.py
```

### 3. Open in Browser
Navigate to: **`http://127.0.0.1:5000/`**

### 4. Start Chatting!
- Click "Chat Here" button
- Type a message
- Press Enter or click Send
- **Watch the sentiment analysis happen!**

## What to Expect

### Message Colors

When you send a message, it will appear with a color based on sentiment:

- 🟢 **Green Background** = Positive/Happy sentiment
  - Examples: "I love this!", "That's great!", "Awesome!"

- 🔴 **Red Background** = Negative/Angry sentiment  
  - Examples: "This is awful.", "I hate it.", "Terrible experience."

- 🟡 **Yellow Background** = Neutral/Factual sentiment
  - Examples: "It's okay.", "This is a fact.", "I think so."

### Interactive Features

**Hover over a message** to see:
- Sentiment emoji (😄 🙂 😐 ☹️ 😠)
- Sentiment category (Very Positive, Positive, Neutral, Negative, Very Negative)
- Full mood description

### Example Messages to Try

| Message | Expected Sentiment | Color |
|---------|---|---|
| "I absolutely love this app!" | Very Positive | 🟢 |
| "This is fantastic!" | Very Positive | 🟢 |
| "I like it!" | Positive | 🟢 |
| "That's nice." | Neutral | 🟡 |
| "This is terrible." | Very Negative | 🔴 |
| "I hate this." | Very Negative | 🔴 |

## Features at a Glance

✅ **Automatic Sentiment Detection** - Analyzes emotion in real-time  
✅ **Color-Coded Messages** - Visual sentiment indicators  
✅ **Hover Descriptions** - See detailed mood info  
✅ **Automatic Storage** - All messages saved to CSV  
✅ **Mood Tracking** - Track sentiment patterns over time  

## File Structure

```
/workspaces/Vit-science-project-/
├── sentiment_analyzer.py           # Core sentiment analysis
├── chat_service.py                 # Chat processing service
├── storage.py                      # CSV storage with sentiment
├── UI.py                           # Flask web server
├── script.js                       # Frontend with sentiment display
├── styles.css                      # Styling with sentiment colors
├── index.html                      # Chat interface
├── chat_history_global.csv         # Message storage (auto-created)
└── SENTIMENT_ANALYSIS_GUIDE.md     # Full documentation
```

## Technical Stack

| Component | Technology |
|-----------|-----------|
| Backend | Python Flask |
| Sentiment Analysis | TextBlob (NLP) |
| Frontend | HTML, CSS, JavaScript |
| Storage | CSV (persistent) |
| Communication | JSON REST API |

## How It Works (Behind the Scenes)

```
1. You type a message and press Enter
   ↓
2. Frontend sends to: POST /api/analyze
   ↓
3. Backend analyzes sentiment using TextBlob
   ↓
4. Backend stores in chat_history_global.csv
   ↓
5. Backend returns sentiment data (color, emoji, description)
   ↓
6. Frontend displays message with sentiment coloring
   ↓
7. You hover to see mood description
```

## Sentiment Polarity Scale

| Polarity Score | Category | Emoji | Example |
|---|---|---|---|
| > 0.3 | Very Positive | 😄 | "I absolutely love this!" |
| 0.1 to 0.3 | Positive | 🙂 | "I like this." |
| -0.1 to 0.1 | Neutral | 😐 | "It's okay." |
| -0.3 to -0.1 | Negative | ☹️ | "I don't like it." |
| < -0.3 | Very Negative | 😠 | "I hate this!" |

## CSV Storage

Every message is automatically saved to `chat_history_global.csv` with:
- Message text
- Sentiment polarity score
- Sentiment category
- Sentiment emoji
- Color code
- Timestamp

**View stored messages**:
```bash
cat chat_history_global.csv
```

## Troubleshooting

### App Won't Start
```bash
# Make sure all dependencies are installed
pip install -r requirements.txt
# Or manually install
pip install flask textblob
python -m textblob.download_corpora
```

### Messages Not Getting Colors
1. Open browser console (F12)
2. Check for errors in Console tab
3. Look at Network tab → check /api/analyze responses
4. Restart Flask: Ctrl+C and `python UI.py` again

### CSV File Issues
- File is created automatically on first message
- Located in the project root directory
- No manual setup needed

## Next Steps

- ✅ Explore different sentiment messages
- ✅ Check the CSV file to see stored messages
- ✅ Read `SENTIMENT_ANALYSIS_GUIDE.md` for full documentation
- ✅ Modify sentiment rules in `sentiment_analyzer.py` if needed
- ✅ Customize colors in `styles.css`

## Support

For more details, see:
- **SENTIMENT_ANALYSIS_GUIDE.md** - Full technical documentation
- **sentiment_analyzer.py** - Source code with inline comments
- **UI.py** - API endpoint documentation

---

**Happy Chatting! 💬✨**
