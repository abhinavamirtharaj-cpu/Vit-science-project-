"""
storage.py - Message storage with sender support
Handles CSV persistence for chat messages with sender information.
"""
import csv
import os
from datetime import datetime
from pathlib import Path

# Get storage file path
STORAGE_FILE = os.path.join(os.path.dirname(__file__), 'chat_history_global.csv')

# CSV Field names
FIELDNAMES = [
    'timestamp', 'contact_id', 'sender', 'direction', 'message',
    'polarity', 'subjectivity', 'category', 'emoji', 'color_hex'
]


def get_csv_path():
    """
    Returns the path to the global CSV storage file.
    """
    return STORAGE_FILE


def append_message(contact, message_data):
    """
    Append a single message to the CSV file with sender information.
    
    Args:
        contact (dict): Contact info with 'id' and 'name'
        message_data (dict): Message details including:
            - text: Message content
            - sender: Username of sender
            - iso: Timestamp
            - sentiment_polarity: Sentiment score
            - sentiment_category: Sentiment category
            - sentiment_emoji: Emoji representation
            - color_hex: Color code for UI
    """
    os.makedirs(os.path.dirname(STORAGE_FILE) or '.', exist_ok=True)
    
    file_exists = os.path.isfile(STORAGE_FILE)
    
    with open(STORAGE_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        
        if not file_exists:
            writer.writeheader()
        
        writer.writerow({
            'timestamp': message_data.get('iso', datetime.now().isoformat()),
            'contact_id': contact.get('id', 'unknown'),
            'sender': message_data.get('sender', 'Unknown'),
            'direction': message_data.get('dir', 'sent'),
            'message': message_data.get('text', ''),
            'polarity': message_data.get('sentiment_polarity', 0),
            'subjectivity': message_data.get('subjectivity', 0),
            'category': message_data.get('sentiment_category', 'Neutral'),
            'emoji': message_data.get('sentiment_emoji', '😐'),
            'color_hex': message_data.get('color_hex', '#9E9E9E')
        })


def append_messages(contact, messages):
    """
    Append multiple messages to the CSV file.
    
    Args:
        contact (dict): Contact info
        messages (list): List of message_data dicts
    """
    for msg in messages:
        append_message(contact, msg)


def get_history(contact_id):
    """
    Retrieve all messages for a specific contact.
    
    Args:
        contact_id (str): Contact identifier
        
    Returns:
        list: List of message dicts with all fields
    """
    if not os.path.isfile(STORAGE_FILE):
        return []
    
    messages = []
    with open(STORAGE_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get('contact_id') == contact_id:
                messages.append({
                    'iso': row.get('timestamp', ''),
                    'sender': row.get('sender', 'Unknown'),
                    'text': row.get('message', ''),
                    'dir': row.get('direction', 'sent'),
                    'sentiment_polarity': float(row.get('polarity', 0)),
                    'sentiment_category': row.get('category', 'Neutral'),
                    'sentiment_emoji': row.get('emoji', '😐'),
                    'color_hex': row.get('color_hex', '#9E9E9E'),
                    'contact_id': row.get('contact_id', '')
                })
    
    return messages


def get_all_messages_for_analysis():
    """
    Retrieve all messages from CSV for sentiment analysis purposes.
    
    Returns:
        list: List of all message dicts
    """
    if not os.path.isfile(STORAGE_FILE):
        return []
    
    messages = []
    with open(STORAGE_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            messages.append({
                'text': row.get('message', ''),
                'sender': row.get('sender', 'Unknown'),
                'timestamp': row.get('timestamp', ''),
                'sentiment': row.get('category', 'Neutral'),
                'polarity': float(row.get('polarity', 0))
            })
    
    return messages


def clear_history(contact_id=None):
    """
    Clear chat history. If contact_id provided, clear only that contact's messages.
    Otherwise, clear all messages.
    
    Args:
        contact_id (str, optional): Specific contact to clear
    """
    if not os.path.isfile(STORAGE_FILE):
        return
    
    if contact_id is None:
        # Clear entire file
        os.remove(STORAGE_FILE)
    else:
        # Keep messages from other contacts
        all_messages = []
        with open(STORAGE_FILE, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get('contact_id') != contact_id:
                    all_messages.append(row)
        
        # Rewrite file
        with open(STORAGE_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            writer.writeheader()
            writer.writerows(all_messages)