"""
chat_service.py - Chat service with sentiment analysis integration

This module integrates storage and sentiment analysis capabilities.
It provides functions to analyze chat messages and persist them with sentiment data.
"""

from storage import append_message, append_messages, get_history, get_csv_path, get_all_messages_for_analysis
from sentiment_analyzer import analyze_chat_message, analyze_historical_context, format_message_for_display

__all__ = [
    "append_message", 
    "append_messages", 
    "get_history", 
    "get_csv_path",
    "get_all_messages_for_analysis",
    "analyze_chat_message",
    "analyze_historical_context",
    "format_message_for_display",
    "process_user_message"
]


def process_user_message(text: str, contact: dict) -> dict:
    """
    Process a user message by analyzing sentiment and formatting for display.
    
    Args:
        text (str): The user's message text
        contact (dict): Contact information with 'id' and 'name'
        
    Returns:
        dict: Processed message with sentiment analysis and display formatting
    """
    # Analyze sentiment
    sentiment_analysis = analyze_chat_message(text)
    
    # Get historical context for trend analysis
    previous_messages = get_all_messages_for_analysis()
    context_analysis = analyze_historical_context(text, previous_messages)
    
    # Format for display
    display_data = format_message_for_display(sentiment_analysis, text)
    
    # Prepare message for storage
    from datetime import datetime
    now = datetime.now()
    message_data = {
        'dir': 'sent',
        'iso': now.isoformat(),
        'date': now.strftime('%Y-%m-%d'),
        'time': now.strftime('%H:%M'),
        'text': text,
        'sentiment_polarity': sentiment_analysis['polarity_score'],
        'sentiment_category': sentiment_analysis['category'],
        'sentiment_emoji': sentiment_analysis['emoji'],
        'color_hex': sentiment_analysis['color']
    }
    
    # Store in CSV
    append_message(contact, message_data)
    
    return {
        'message': display_data,
        'sentiment': sentiment_analysis,
        'trend': context_analysis.get('sentiment_trend'),
        'stored': True
    }

