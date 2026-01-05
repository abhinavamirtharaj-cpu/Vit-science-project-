"""
node_3.py
Core Analysis System Node.

This processing node:
- Analyzes message context.
- Evaluates historical user responses.
- Generates composite sentiment scores.
- Implements weighted decision-making between node-1 and node-2.
- Applies dynamic biases.
"""

import random

# Sentiment Constants
SENTIMENT_RANGES = {
    'Very Positive': (0.6, 1.0),
    'Positive': (0.2, 0.6),
    'Neutral': (-0.2, 0.2),
    'Negative': (-0.6, -0.2),
    'Very Negative': (-1.0, -0.6)
}

COLORS = {
    'Very Positive': '\033[92m', # Green
    'Positive': '\033[96m',      # Cyan
    'Neutral': '\033[93m',       # Yellow
    'Negative': '\033[91m',      # Red
    'Very Negative': '\033[95m', # Magenta
    'Sarcastic': '\033[94m',     # Blue
    'RESET': '\033[0m'
}

def analyze_context(text, history_messages):
    """
    Analyzes message context within specified sentiment score ranges.
    Simple keyword/heuristic analysis since Node 1 is empty.
    """
    # Simple heuristic context analysis
    text_lower = text.lower()
    
    # Sarcasm detection (Rudimentary)
    sarcasm_indicators = ["oh great", "thanks a lot", "yeah right", "wow"]
    is_sarcastic = any(phrase in text_lower for phrase in sarcasm_indicators) and ("!" in text or "..." in text)
    
    # Keyword based base score (fallback for Node 1)
    base_score = 0.0
    positive_words = ["good", "great", "happy", "love", "excellent", "thanks"]
    negative_words = ["bad", "hate", "terrible", "sad", "angry", "worst"]
    
    for word in positive_words:
        if word in text_lower:
            base_score += 0.3
            
    for word in negative_words:
        if word in text_lower:
            base_score -= 0.3
            
    # Clamp score
    base_score = max(min(base_score, 1.0), -1.0)
    
    return {
        'context_score': base_score,
        'is_sarcastic': is_sarcastic
    }

def apply_dynamic_biases(current_score, prediction_data):
    """
    Applies dynamic biases throughout the analysis process.
    Biases the score towards the predicted next sentiment if available.
    """
    if not prediction_data or not prediction_data.get('prediction'):
        return current_score
        
    predicted_sentiment = prediction_data['prediction']
    probability = prediction_data['probability']
    
    # Bias weights
    bias = 0.0
    if predicted_sentiment in ['Very Positive', 'Positive']:
        bias = 0.2 * probability
    elif predicted_sentiment in ['Very Negative', 'Negative']:
        bias = -0.2 * probability
        
    return current_score + bias

def get_sentiment_category(score, is_sarcastic):
    if is_sarcastic:
        return 'Sarcastic'
        
    for category, (low, high) in SENTIMENT_RANGES.items():
        if low <= score <= high:
            return category
            
    # Edge cases
    if score > 1.0: return 'Very Positive'
    if score < -1.0: return 'Very Negative'
    return 'Neutral'

def run_core_analysis(text, node_1_result, node_2_result, history_messages):
    """
    Main entry point for Node 3.
    Implements weighted decision-making.
    """
    print(f"DEBUG: Node 3 Analyzing: '{text}'")
    
    # 1. Context Analysis
    context_data = analyze_context(text, history_messages)
    context_score = context_data['context_score']
    is_sarcastic = context_data['is_sarcastic']
    
    # 2. Evaluate Node 1 (TextBlob) - Currently Empty/None
    node_1_score = 0.0
    w1 = 0.0
    if node_1_result:
        node_1_score = node_1_result.get('polarity', 0.0)
        w1 = 0.6 # High weight for actual text analysis if available
    
    # 3. Evaluate Node 2 (Prediction)
    # Node 2 gives a prediction of what comes *next*, but we can use it 
    # to check if the current text aligns with expectation (Pattern Matching).
    # Here we use it to bias the context score.
    
    # 4. Generate Composite Score
    # Since Node 1 is empty, we rely on Context Analysis (w_context) and Node 2 Bias.
    w_context = 1.0 if w1 == 0 else 0.4
    
    raw_score = (node_1_score * w1) + (context_score * w_context)
    
    # 5. Apply Dynamic Biases (using Node 2)
    final_score = apply_dynamic_biases(raw_score, node_2_result)
    
    # 6. Classification
    category = get_sentiment_category(final_score, is_sarcastic)
    
    # 7. Formatting Output
    color = COLORS.get(category, COLORS['RESET'])
    
    return {
        'composite_score': final_score,
        'category': category,
        'color_code': color,
        'is_sarcastic': is_sarcastic,
        'node_2_prediction': node_2_result.get('prediction'),
        'description': f"Score: {final_score:.2f} ({category})"
    }
