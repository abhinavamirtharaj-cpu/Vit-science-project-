"""
storage.py
A simple CSV-backed storage module to append and read chat messages with sentiment analysis.
Functions:
- append_message(contact, message): append single message with optional sentiment data
- append_messages(contact, messages): append list of message dicts to CSV
- get_history(contact_id): return list of messages for contact_id
- get_csv_path(): return path to csv file
- get_all_messages_for_analysis(): get all messages for sentiment context analysis
This module is importable and can be used by other Python modules/devices.
"""
import csv
import os
from datetime import datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(ROOT, 'chat_history_global.csv')

CSV_HEADER = ['contact_id','contact_name','dir','iso_time','date','time','text','sentiment_polarity','sentiment_category','sentiment_emoji','color_hex','saved_at']


def _ensure_header():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(CSV_HEADER)


def append_message(contact, message):
    """Append a single message dict to CSV with optional sentiment data.
    contact: dict with keys 'id' and optional 'name'
    message: dict with keys 'dir','iso','date','time','text', and optional sentiment data
    """
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
    """Return list of messages for contact_id (ordered by file order)."""
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
    """Return all messages for sentiment context analysis."""
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