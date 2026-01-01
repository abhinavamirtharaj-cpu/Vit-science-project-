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
