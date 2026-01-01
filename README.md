# Message Sentiment Analyzer with Encryption

## Project Overview
Reads messages from a messaging app, performs sentiment analysis (positive/negative/neutral), color-codes them (green/red/yellow), and sends encrypted reports to developers. Built for VIT Science project. [web:116][web:122]

## Features
- Real-time sentiment analysis using VADER/TextBlob
- Color coding: Green (positive), Yellow (neutral), Red (negative)
- End-to-end encryption for privacy
- Generates analysis reports

## How it works
1. Fetch messages from app (API/export)
2. Analyze sentiment → assign colors
3. Encrypt analysis data
4. Send secure report to developer

## Tech Stack
- Python 3.x
- NLTK/TextBlob (sentiment)
- Fernet (encryption)
- Matplotlib/Streamlit (visualization)

## Setup

### Run the chat UI server (dev)
1. Create & activate a virtual environment (optional):
   - python -m venv .venv
   - .\.venv\Scripts\Activate.ps1
2. Install dependencies:
   - pip install flask
3. Start the static UI server (serves `index.html` and assets):
   - python UI.py
4. Open in browser: http://127.0.0.1:5000/

CSV persistence
- The project includes `storage.py` which provides a simple CSV-backed API (`append_message`, `append_messages`, `get_history`, `get_csv_path`) that other Python modules can import to persist chat data to `chat_history_global.csv`.

(If you previously used `socketio_client.py` or `test_client.py` those demo clients have been removed; import `storage.py` directly for integrations.)

