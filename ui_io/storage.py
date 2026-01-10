"""
storage.py
A unified storage module supporting both CSV and PostgreSQL backends.
Automatically uses PostgreSQL if DATABASE_URL is set, otherwise falls back to CSV.

Functions:
- append_message(contact, message): append single message with optional sentiment data
- append_messages(contact, messages): append list of message dicts
- get_history(contact_id): return list of messages for contact_id
- get_csv_path(): return path to csv file (CSV mode only)
- get_all_messages_for_analysis(): get all messages for sentiment context analysis

This module is importable and can be used by other Python modules/devices.
"""

import csv
import os
from datetime import datetime
from get_resource_path import get_resource_path

# Try to import database module
try:
    from ui_io.database import (
        init_db, is_db_enabled, 
        append_message_db, get_history_db, get_all_messages_db
    )
    DB_AVAILABLE = True
except ImportError:
    DB_AVAILABLE = False
    print("Database module not available, using CSV only")

CSV_FILE = get_resource_path(os.path.join('models', 'chat_history_global.csv'))

CSV_HEADER = ['contact_id','contact_name','dir','iso_time','date','time','text','sentiment_polarity','sentiment_category','sentiment_emoji','color_hex','saved_at']

# Initialize database on module import
_USE_DB = False
if DB_AVAILABLE:
    _USE_DB = init_db()
    if _USE_DB:
        print("✓ Using PostgreSQL database for storage")
    else:
        print("✓ Using CSV file for storage")
else:
    print("✓ Using CSV file for storage")


def _ensure_header():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(CSV_HEADER)


def append_message(contact, message):
    """Append a single message dict with optional sentiment data.
    Automatically uses PostgreSQL if available, otherwise CSV.
    contact: dict with keys 'id' and optional 'name'
    message: dict with keys 'dir','iso','date','time','text', and optional sentiment data
    """
    # Try database first
    if _USE_DB:
        if append_message_db(contact, message):
            return
        # Fall through to CSV on database error
    
    # CSV fallback
    _ensure_header()
    with open(CSV_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            contact.get('id'),
            contact.get('name'),
            message.get('dir'),
            message.get('iso') or '',
            message.get('date') or '',
            message.get('time') or '',
            message.get('text') or '',
            message.get('sentiment_polarity') or '',
            message.get('sentiment_category') or '',
            message.get('sentiment_emoji') or '',
            message.get('color_hex') or '',
            datetime.utcnow().isoformat()
        ])


def append_messages(contact, messages):
    """Append multiple messages. Uses database if available, otherwise CSV."""
    # Try database first
    if _USE_DB:
        for m in messages:
            append_message_db(contact, m)
        return
    
    # CSV fallback
    _ensure_header()
    with open(CSV_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        for m in messages:
            writer.writerow([
                contact.get('id'),
                contact.get('name'),
                m.get('dir'),
                m.get('iso') or '',
                m.get('date') or '',
                m.get('time') or '',
                m.get('text') or '',
                m.get('sentiment_polarity') or '',
                m.get('sentiment_category') or '',
                m.get('sentiment_emoji') or '',
                m.get('color_hex') or '',
                datetime.utcnow().isoformat()
            ])


def get_history(contact_id):
    """Return list of messages for contact_id. Uses database if available."""
    # Try database first
    if _USE_DB:
        return get_history_db(contact_id)
    
    # CSV fallback
    if not os.path.exists(CSV_FILE):
        return []
    out = []
    with open(CSV_FILE, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get('contact_id') == str(contact_id):
                out.append({
                    'dir': row.get('dir'),
                    'iso': row.get('iso_time'),
                    'date': row.get('date'),
                    'time': row.get('time'),
                    'text': row.get('text'),
                    'sentiment_polarity': row.get('sentiment_polarity') or None,
                    'sentiment_category': row.get('sentiment_category') or None,
                    'sentiment_emoji': row.get('sentiment_emoji') or None,
                    'color_hex': row.get('color_hex') or None
                })
    return out


def get_all_messages_for_analysis():
    """Return all messages for sentiment context analysis. Uses database if available."""
    # Try database first
    if _USE_DB:
        db_messages = get_all_messages_db()
        return [msg['text'] for msg in db_messages if msg.get('text')]
    
    # CSV fallback
    if not os.path.exists(CSV_FILE):
        return []
    messages = []
    with open(CSV_FILE, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get('text'):
                messages.append(row.get('text'))
    return messages


def get_csv_path():
    return CSV_FILE


if __name__ == '__main__':
    print('CSV path:', CSV_FILE)
    _ensure_header()
    print('Header ensured.')