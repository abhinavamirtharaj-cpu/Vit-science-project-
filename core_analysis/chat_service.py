"""
chat_service.py - Chat service with sentiment analysis integration

This module integrates storage and sentiment analysis capabilities.
It provides functions to analyze chat messages and persist them with sentiment data.
Supports both emotion-based and sentiment category-based analysis.
"""
import sys
import os

# Add parent directory to path to find other modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ui_io.storage import append_message, append_messages, get_history, get_csv_path, get_all_messages_for_analysis
from core_analysis.node_1 import analyze_sentiment_node_1
from core_analysis.node_2 import run_node_2_analysis
from core_analysis.node_3 import run_core_analysis

# Import emotion detection
try:
    from emotion_analyzer import analyze_emotion
    from emotion_colors import EMOTION_COLORS, EMOTION_EMOJIS, get_emotion_category
    EMOTION_MODE = True
except ImportError:
    EMOTION_MODE = False
    print("Warning: Emotion detection not available, using sentiment categories")

__all__ = [
    "append_message", 
    "append_messages", 
    "get_history", 
    "get_csv_path",
    "get_all_messages_for_analysis",
    "process_user_message",
    "predict_next_sentiment",
    "get_last_sentiment_from_history"
]


def get_last_sentiment_from_history(contact_id: str):
    """
    Retrieves the last recorded sentiment for a contact from the CSV history.
    """
    history = get_history(contact_id)
    # Iterate backwards to find the last 'sent' message with sentiment
    for msg in reversed(history):
        if msg.get('dir') == 'sent' and msg.get('sentiment_category'):
            return msg.get('sentiment_category')
    return None


def predict_next_sentiment(current_sentiment: str):
    """
    Predicts the next sentiment based on the current one using the CSV history.
    Uses Node 2.
    """
    csv_path = get_csv_path()
    result = run_node_2_analysis(csv_path, current_sentiment)
    return result.get('prediction'), result.get('probability')


def process_user_message(text: str, contact: dict) -> dict:
    """
    Process a user message by analyzing sentiment/emotion and formatting for display.
    Uses the Node 1, 2, 3 Architecture.
    
    Args:
        text (str): The user's message text
        contact (dict): Contact information with 'id' and 'name'
        
    Returns:
        dict: Processed message with sentiment/emotion analysis and display formatting
    """
    # 1. Get History
    csv_path = get_csv_path()
    history_messages = get_all_messages_for_analysis()
    
    # Get last sentiment for Node 2 prediction context
    last_sentiment = get_last_sentiment_from_history(contact.get('id', 'unknown'))
    if not last_sentiment:
        last_sentiment = 'Neutral'
        
    # 2. Run Node 2 (Prediction)
    node_2_result = run_node_2_analysis(csv_path, last_sentiment)
    
    # 3. Run Node 1 (Placeholder)
    node_1_result = analyze_sentiment_node_1(text)
    
    # 4. Check if emotion mode is enabled
    if EMOTION_MODE:
        # Get contact's chat history for context-aware emotion detection
        contact_history = get_history(contact.get('id', 'unknown'))
        
        # Use emotion detection with chat history for more granular analysis
        emotion_result = analyze_emotion(text, contact_history)
        emotion_label = emotion_result['emotion']
        category = emotion_result['category']
        polarity = emotion_result['polarity']
        
        sentiment_analysis = {
            'polarity_score': polarity,
            'category': emotion_label,  # Return specific emotion
            'emotion': emotion_label,
            'emoji': EMOTION_EMOJIS.get(emotion_label, '😐'),
            'color': EMOTION_COLORS.get(emotion_label, '#90A4AE'),
            'description': f'Detected emotion: {emotion_label} (context-aware)'
        }
    else:
        # 5. Run Node 3 (Core Analysis) - Use traditional sentiment categories
        final_result = run_core_analysis(text, node_1_result, node_2_result, history_messages)
        
        # Format for display/storage
        sentiment_analysis = {
            'polarity_score': final_result['composite_score'],
            'category': final_result['category'],
            'emotion': None,
            'emoji': '🤔' if final_result['category'] == 'Sarcastic' else '',
            'color': '#333333',
            'description': final_result['description']
        }
        
        # Enhance Emoji/Color mapping from Node 3 categories
        emoji_map = {
            'Very Positive': '😄', 'Positive': '🙂', 'Neutral': '😐', 
            'Negative': '☹️', 'Very Negative': '😠', 'Sarcastic': '😏'
        }
        # Vibrant color scheme for each sentiment category
        hex_map = {
            'Very Positive': '#00E676',   # Bright green
            'Positive': '#2196F3',        # Bright blue
            'Neutral': '#FFC107',         # Amber/yellow
            'Negative': '#FF5722',        # Deep orange/red
            'Very Negative': '#E91E63',   # Pink/magenta
            'Sarcastic': '#9C27B0'        # Purple
        }
        
        sentiment_analysis['emoji'] = emoji_map.get(final_result['category'], '😐')
        sentiment_analysis['color'] = hex_map.get(final_result['category'], '#9E9E9E')
    
    
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
    
    # Display Data for UI
    display_data = {
        'text': text,
        'sentiment': sentiment_analysis
    }
    
    return {
        'message': display_data,
        'sentiment': sentiment_analysis,
        'trend': 'stable', # Simplified for now
        'stored': True
    }
