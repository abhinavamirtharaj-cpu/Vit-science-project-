"""
node_1.py
TextBlob-based Sentiment Analysis Node.

Analyzes text sentiment using TextBlob NLP library.
Returns polarity, subjectivity, and sentiment classification.
"""

try:
    from textblob import TextBlob
    TEXTBLOB_AVAILABLE = True
except ImportError:
    TEXTBLOB_AVAILABLE = False
    print("Warning: TextBlob not available. Using fallback sentiment analysis.")

def analyze_sentiment_node_1(text):
    """
    Analyze text sentiment using TextBlob.
    
    Args:
        text (str): The input text to analyze.
        
    Returns:
        dict: Sentiment analysis results with polarity, subjectivity, and category.
    """
    if not text or not isinstance(text, str):
        return {
            'polarity': 0.0,
            'subjectivity': 0.0,
            'sentiment_category': 'Neutral',
            'source': 'node_1'
        }
    
    if TEXTBLOB_AVAILABLE:
        try:
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity
            subjectivity = blob.sentiment.subjectivity
        except Exception as e:
            # Fallback if TextBlob fails
            polarity = 0.0
            subjectivity = 0.5
    else:
        # Simple fallback based on keywords
        polarity = calculate_polarity_fallback(text)
        subjectivity = 0.5
    
    # Map polarity to sentiment category
    if polarity > 0.3:
        sentiment_category = 'Very Positive'
    elif polarity > 0.1:
        sentiment_category = 'Positive'
    elif polarity < -0.3:
        sentiment_category = 'Very Negative'
    elif polarity < -0.1:
        sentiment_category = 'Negative'
    else:
        sentiment_category = 'Neutral'
    
    return {
        'polarity': polarity,
        'subjectivity': subjectivity,
        'sentiment_category': sentiment_category,
        'source': 'node_1'
    }

def calculate_polarity_fallback(text):
    """Simple keyword-based polarity calculation as fallback"""
    text_lower = text.lower().strip()
    
    # Common neutral greetings should always return 0.0
    neutral_greetings = ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening',
                         'greetings', 'howdy', 'sup', 'yo', 'hola', 'bonjour']
    if text_lower in neutral_greetings:
        return 0.0
    
    positive_words = ['good', 'great', 'excellent', 'amazing', 'love', 'happy', 'thanks', 'wonderful', 'fantastic']
    negative_words = ['bad', 'terrible', 'hate', 'awful', 'worst', 'disappointed', 'angry', 'sad', 'frustrated']
    
    pos_count = sum(1 for word in positive_words if word in text_lower)
    neg_count = sum(1 for word in negative_words if word in text_lower)
    
    total_words = len(text.split())
    if total_words == 0:
        return 0.0
    
    score = (pos_count - neg_count) / max(total_words, 1)
    return max(-1.0, min(1.0, score * 2))  # Scale and clamp

# CONNECTION POINT FOR FUTURE CODE: Helper functions for TextBlob
