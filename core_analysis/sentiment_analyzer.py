"""
sentiment_analyzer.py
Advanced sentiment analysis module for chat messages.

Features:
- Analyzes sentiment polarity and subjectivity using TextBlob
- Maps sentiment to color codes and descriptions
- Returns structured sentiment data for UI display
- Supports historical context analysis
"""

from textblob import TextBlob
import json
from typing import Dict, Tuple, List


def analyze_emotion(text: str) -> Tuple[float, float]:
    """
    Analyzes the sentiment of the text using TextBlob.
    
    Args:
        text (str): The input text to analyze
        
    Returns:
        tuple: (polarity, subjectivity)
            - Polarity: -1 (negative) to 1 (positive)
            - Subjectivity: 0 (objective) to 1 (subjective)
    """
    blob = TextBlob(text)
    return blob.sentiment.polarity, blob.sentiment.subjectivity


def get_sentiment_color(polarity: float) -> str:
    """
    Maps polarity to a color code for HTML/CSS.
    
    Args:
        polarity (float): Sentiment polarity value (-1 to 1)
        
    Returns:
        str: Hex color code
            - Positive (>0.1): Green (#4CAF50)
            - Negative (<-0.1): Red (#F44336)
            - Neutral: Yellow/Amber (#FFC107)
    """
    if polarity > 0.1:
        return "#4CAF50"  # Green
    elif polarity < -0.1:
        return "#F44336"  # Red
    else:
        return "#FFC107"  # Yellow/Amber


def get_sentiment_category(polarity: float) -> Dict[str, str]:
    """
    Maps polarity to sentiment category with emoji and description.
    
    Args:
        polarity (float): Sentiment polarity value (-1 to 1)
        
    Returns:
        dict: Contains 'emoji', 'category', and 'description'
    """
    if polarity > 0.3:
        return {
            "emoji": "😄",
            "category": "Very Positive",
            "description": "Expressing great joy, enthusiasm, or satisfaction"
        }
    elif polarity > 0.1:
        return {
            "emoji": "🙂",
            "category": "Positive",
            "description": "Expressing happiness, contentment, or approval"
        }
    elif polarity > -0.1:
        return {
            "emoji": "😐",
            "category": "Neutral",
            "description": "Expressing factual information or neutral sentiment"
        }
    elif polarity > -0.3:
        return {
            "emoji": "☹️",
            "category": "Negative",
            "description": "Expressing dissatisfaction, doubt, or disappointment"
        }
    else:
        return {
            "emoji": "😠",
            "category": "Very Negative",
            "description": "Expressing strong anger, frustration, or disappointment"
        }


def analyze_chat_message(text: str) -> Dict:
    """
    Comprehensive sentiment analysis for a chat message.
    
    Args:
        text (str): The chat message text
        
    Returns:
        dict: Comprehensive sentiment analysis with:
            - input_text: Original text
            - polarity_score: Sentiment polarity (-1 to 1)
            - subjectivity_score: Subjectivity (0 to 1)
            - color: Hex color code
            - emoji: Sentiment emoji
            - category: Sentiment category
            - description: Sentiment description
            - is_positive: Boolean indicator
    """
    polarity, subjectivity = analyze_emotion(text)
    sentiment_info = get_sentiment_category(polarity)
    
    result = {
        "input_text": text,
        "polarity_score": round(polarity, 3),
        "subjectivity_score": round(subjectivity, 3),
        "color": get_sentiment_color(polarity),
        "emoji": sentiment_info["emoji"],
        "category": sentiment_info["category"],
        "description": sentiment_info["description"],
        "is_positive": polarity > 0.1,
        "is_negative": polarity < -0.1,
        "is_neutral": -0.1 <= polarity <= 0.1
    }
    
    return result


def analyze_historical_context(current_message: str, previous_messages: List[str]) -> Dict:
    """
    Analyzes sentiment of current message with context from previous messages.
    Helps understand sentiment trends and patterns.
    
    Args:
        current_message (str): The current message to analyze
        previous_messages (list): List of previous message texts
        
    Returns:
        dict: Analysis with context insights
    """
    current_analysis = analyze_chat_message(current_message)
    
    # Analyze previous messages for context
    previous_polarities = []
    if previous_messages:
        for msg in previous_messages[-5:]:  # Last 5 messages for context
            _, pol = analyze_emotion(msg)
            previous_polarities.append(pol)
    
    # Calculate trend
    trend = "neutral"
    if previous_polarities:
        avg_previous = sum(previous_polarities) / len(previous_polarities)
        current_pol = current_analysis["polarity_score"]
        
        if current_pol > avg_previous + 0.1:
            trend = "improving"
        elif current_pol < avg_previous - 0.1:
            trend = "declining"
        else:
            trend = "stable"
    
    current_analysis["sentiment_trend"] = trend
    current_analysis["context_count"] = len(previous_polarities)
    
    return current_analysis


def batch_analyze_messages(messages: List[str]) -> List[Dict]:
    """
    Analyzes multiple messages at once.
    
    Args:
        messages (list): List of message texts
        
    Returns:
        list: List of sentiment analysis dictionaries
    """
    return [analyze_chat_message(msg) for msg in messages]


def format_message_for_display(analysis: Dict, text: str) -> Dict:
    """
    Formats sentiment analysis data for frontend display.
    
    Args:
        analysis (dict): Result from analyze_chat_message()
        text (str): The message text
        
    Returns:
        dict: Formatted data ready for HTML rendering
    """
    return {
        "text": text,
        "sentiment": {
            "emoji": analysis["emoji"],
            "category": analysis["category"],
            "description": analysis["description"],
            "color": analysis["color"],
            "polarity": analysis["polarity_score"],
            "subjectivity": analysis["subjectivity_score"]
        },
        "is_positive": analysis["is_positive"],
        "is_negative": analysis["is_negative"],
        "is_neutral": analysis["is_neutral"]
    }


if __name__ == "__main__":
    # Test the module
    test_messages = [
        "I love this messaging app!",
        "Terrible service, full of bugs.",
        "It's okay, works fine.",
        "This is absolutely amazing!",
        "I hate this, worst experience ever."
    ]
    
    print("=" * 70)
    print("SENTIMENT ANALYSIS TEST")
    print("=" * 70)
    
    analyses = batch_analyze_messages(test_messages)
    
    for i, analysis in enumerate(analyses, 1):
        print(f"\n[{i}] {analysis['input_text']}")
        print(f"    Category: {analysis['emoji']} {analysis['category']}")
        print(f"    Polarity: {analysis['polarity_score']:.3f} | Subjectivity: {analysis['subjectivity_score']:.3f}")
        print(f"    Description: {analysis['description']}")
        print(f"    Color: {analysis['color']}")
    
    print("\n" + "=" * 70)
    print("FULL JSON OUTPUT")
    print("=" * 70)
    print(json.dumps(analyses, indent=2))
