"""
storage.py - Message storage with sender support for two-person chat

Handles CSV persistence for chat messages with sentiment data and sender information.
"""
import os
import csv
from datetime import datetime

STORAGE_FILE = os.path.join(os.path.dirname(__file__), 'chat_history_global.csv')


def get_csv_path():
    """Returns the path to the global CSV storage file."""
    return STORAGE_FILE


def append_message(contact: dict, msg: dict):
    """
    Append a single message to the CSV file.
    
    Args:
        contact (dict): Contact information with 'id' and 'name'
        msg (dict): Message data with sentiment information
    """
    os.makedirs(os.path.dirname(STORAGE_FILE) or '.', exist_ok=True)
    
    file_exists = os.path.isfile(STORAGE_FILE)
    
    with open(STORAGE_FILE, 'a', newline='', encoding='utf-8') as f:
        fieldnames = [
            'contact_id', 'contact_name', 'dir', 'iso', 'date', 'time', 'text',
            'sender', 'sentiment_polarity', 'sentiment_category', 'sentiment_emoji', 'color_hex'
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        
        if not file_exists:
            writer.writeheader()
        
        row = {
            'contact_id': contact.get('id', 'unknown'),
            'contact_name': contact.get('name', 'Unknown'),
            'dir': msg.get('dir', 'sent'),
            'iso': msg.get('iso', datetime.now().isoformat()),
            'date': msg.get('date', datetime.now().strftime('%Y-%m-%d')),
            'time': msg.get('time', datetime.now().strftime('%H:%M')),
            'text': msg.get('text', ''),
            'sender': msg.get('sender', 'Unknown'),
            'sentiment_polarity': msg.get('sentiment_polarity', 0),
            'sentiment_category': msg.get('sentiment_category', 'Neutral'),
            'sentiment_emoji': msg.get('sentiment_emoji', '😐'),
            'color_hex': msg.get('color_hex', '#9E9E9E')
        }
        
        writer.writerow(row)


def append_message_with_sender(contact: dict, msg: dict):
    """
    Append message with explicit sender information.
    Wrapper for append_message to ensure sender is included.
    
    Args:
        contact (dict): Contact information
        msg (dict): Message data including 'sender' field
    """
    append_message(contact, msg)


def append_messages(contact: dict, msgs: list):
    """
    Append multiple messages to the CSV file.
    
    Args:
        contact (dict): Contact information
        msgs (list): List of message dictionaries
    """
    for msg in msgs:
        append_message(contact, msg)


def get_history(contact_id: str) -> list:
    """
    Retrieve all messages for a specific contact from CSV.
    
    Args:
        contact_id (str): The contact/room ID
        
    Returns:
        list: List of message dictionaries
    """
    if not os.path.isfile(STORAGE_FILE):
        return []
    
    messages = []
    
    try:
        with open(STORAGE_FILE, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get('contact_id') == contact_id:
                    messages.append(row)
    except Exception as e:
        print(f"[Error] Failed to read chat history: {str(e)}")
        return []
    
    return messages


def get_all_messages_for_analysis() -> list:
    """
    Retrieve all messages from CSV for sentiment analysis.
    
    Returns:
        list: List of all messages
    """
    if not os.path.isfile(STORAGE_FILE):
        return []
    
    messages = []
    
    try:
        with open(STORAGE_FILE, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                messages.append(row)
    except Exception as e:
        print(f"[Error] Failed to read messages for analysis: {str(e)}")
        return []
    
    return messages


def clear_history(contact_id: str = None):
    """
    Clear chat history. If contact_id is provided, clear only that contact.
    Otherwise, clear entire history.
    
    Args:
        contact_id (str, optional): Contact ID to clear, or None for all
    """
    if not os.path.isfile(STORAGE_FILE):
        return
    
    if contact_id is None:
        # Clear entire file
        os.remove(STORAGE_FILE)
        return
    
    # Clear specific contact
    messages = []
    with open(STORAGE_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get('contact_id') != contact_id:
                messages.append(row)
    
    # Rewrite file without the contact's messages
    if messages:
        with open(STORAGE_FILE, 'w', newline='', encoding='utf-8') as f:
            fieldnames = [
                'contact_id', 'contact_name', 'dir', 'iso', 'date', 'time', 'text',
                'sender', 'sentiment_polarity', 'sentiment_category', 'sentiment_emoji', 'color_hex'
            ]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(messages)
    else:
        os.remove(STORAGE_FILE)