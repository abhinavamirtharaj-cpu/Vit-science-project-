"""
node_3.py
Core Analysis System Node (User Insight Engine).

This processing node:
- Analyzes message context.
- Evaluates historical user responses to different sentiment scores.
- Generates composite sentiment scores.
- Implements weighted decision-making between node-1 and node-2 outputs.
- Applies dynamic biases throughout the analysis process.
- Stores analysis in a local database (JSON) to build a knowledge base.
- Impersonates user emotions based on insights.
"""

import random
import json
import os
import datetime
from collections import defaultdict
import re

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

class UserInsightEngine:
    def __init__(self):
        self.db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'user_insights.json')
        self.insights = self._load_db()

    def _load_db(self):
        if os.path.exists(self.db_path):
            try:
                with open(self.db_path, 'r') as f:
                    return json.load(f)
            except:
                return {"interactions": [], "patterns": {}}
        return {"interactions": [], "patterns": {}}

    def _save_db(self):
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        with open(self.db_path, 'w') as f:
            json.dump(self.insights, f, indent=4)

    def track_interaction(self, user_text, sentiment_category, node_1_score, node_2_prediction, final_score):
        """
        Stores analysis of previous checks to build a knowledge base.
        """
        interaction = {
            "timestamp": datetime.datetime.now().isoformat(),
            "text": user_text,
            "sentiment": sentiment_category,
            "score": final_score,
            "node_1_input": node_1_score,
            "node_2_prediction": node_2_prediction
        }
        self.insights["interactions"].append(interaction)
        
        # Update patterns: How does user respond to different contexts?
        # Simple pattern: Count frequency of sentiments
        if "sentiment_counts" not in self.insights["patterns"]:
            self.insights["patterns"]["sentiment_counts"] = {}
        
        counts = self.insights["patterns"]["sentiment_counts"]
        counts[sentiment_category] = counts.get(sentiment_category, 0) + 1
        
        self._save_db()

    def get_user_impersonation_profile(self):
        """
        Returns the most accurate approach/emotion the user follows.
        """
        counts = self.insights["patterns"].get("sentiment_counts", {})
        if not counts:
            return "Neutral"
        
        # Find dominant sentiment
        dominant = max(counts, key=counts.get)
        return dominant

def detect_factual(text):
    t = text.strip().lower()
    patterns = [
        r"\b\d{1,2}[:/.-]\d{1,2}([/:.-]\d{2,4})?\b",
        r"\b\d+\b",
        r"\bversion\s+\d+(\.\d+)*\b",
        r"\b(is|are|was|were|will be)\b",
        r"\bthe capital of\b",
        r"\bdefinition\b",
        r"\bpercentage\b",
        r"\bunit\b",
        r"\bkm\b|\bkg\b|\bmb\b"
    ]
    for p in patterns:
        if re.search(p, t):
            return True
    factual_keywords = ["account balance", "order number", "tracking id", "reference"]
    if any(k in t for k in factual_keywords):
        return True
    return False

def analyze_context(text, history_messages):
    """
    Analyzes message context within specified sentiment score ranges.
    """
    text_lower = text.lower()
    
    sarcasm_indicators = ["oh great", "thanks a lot", "yeah right", "wow"]
    is_sarcastic = any(phrase in text_lower for phrase in sarcasm_indicators) and ("!" in text or "..." in text)
    
    base_score = 0.0
    positive_words = ["good", "great", "happy", "love", "excellent", "thanks", "amazing", "best", "fantastic"]
    negative_words = ["bad", "hate", "terrible", "sad", "angry", "worst", "awful", "broken", "refund", "slow", "hell", "damn", "wtf", "fish"]
    interjection_negatives = ["what the hell", "what the fish", "wtf", "damn", "screw this", "this sucks"]
    
    pos_count = 0
    neg_count = 0
    for word in positive_words:
        if word in text_lower:
            base_score += 0.3
            pos_count += 1
            
    for word in negative_words:
        if word in text_lower:
            base_score -= 0.3
            neg_count += 1

    for phrase in interjection_negatives:
        if phrase in text_lower:
            base_score -= 0.4
            neg_count += 1

    exclamations = text.count("!")
    if exclamations > 0:
        if neg_count > 0:
            base_score -= min(0.2 + 0.1 * (exclamations - 1), 0.5)
        elif pos_count > 0:
            base_score += min(0.2 + 0.1 * (exclamations - 1), 0.5)
            
    base_score = max(min(base_score, 1.0), -1.0)
    
    return {
        'context_score': base_score,
        'is_sarcastic': is_sarcastic,
        'pos_count': pos_count,
        'neg_count': neg_count
    }

def apply_dynamic_biases(current_score, prediction_data, insight_engine):
    """
    Applies dynamic biases using Node 2 prediction and Historical Insights.
    """
    bias = 0.0
    
    # 1. Node 2 Prediction Bias
    if prediction_data and prediction_data.get('prediction'):
        predicted_sentiment = prediction_data['prediction']
        probability = prediction_data.get('probability', 0.5)
        
        if predicted_sentiment in ['Very Positive', 'Positive']:
            bias += 0.2 * probability
        elif predicted_sentiment in ['Very Negative', 'Negative']:
            bias -= 0.2 * probability

    # 2. Historical Insight Bias (Impersonation)
    dominant_sentiment = insight_engine.get_user_impersonation_profile()
    if dominant_sentiment in ['Very Positive', 'Positive']:
        bias += 0.05 # Slight positive tilt if user is generally happy
    elif dominant_sentiment in ['Very Negative', 'Negative']:
        bias -= 0.05

    return current_score + bias

def get_sentiment_category(score, is_sarcastic, pos_count, neg_count, is_factual):
    if is_sarcastic:
        return 'Sarcastic'
    # Treat factual-without-emotion as Neutral, not a separate label
    if is_factual and pos_count == 0 and neg_count == 0:
        if -0.2 <= score <= 0.2:
            return 'Neutral'
        # If numbers present but clear emotion, fall through to emotion classification
    if neg_count > pos_count:
        if score <= -0.6:
            return 'Very Negative'
        if score <= -0.2:
            return 'Negative'
        return 'Negative'
    if pos_count > neg_count:
        if score >= 0.6:
            return 'Very Positive'
        if score >= 0.2:
            return 'Positive'
        return 'Positive'
    if score >= 0.6:
        return 'Very Positive'
    if 0.2 <= score < 0.6:
        return 'Positive'
    if -0.6 <= score < -0.2:
        return 'Negative'
    if score < -0.6:
        return 'Very Negative'
    # Default: Neutral when signals are weak or balanced
    return 'Neutral'

# Singleton Engine
engine = UserInsightEngine()

def run_core_analysis(text, node_1_result, node_2_result, history_messages):
    """
    Main entry point for Node 3.
    Integrates Node 1, Node 2, and Insight Engine.
    """
    # print(f"DEBUG: Node 3 Analyzing: '{text}'")
    
    # 1. Context Analysis
    context_data = analyze_context(text, history_messages)
    context_score = context_data['context_score']
    is_sarcastic = context_data['is_sarcastic']
    pos_count = context_data['pos_count']
    neg_count = context_data['neg_count']
    is_factual = detect_factual(text)
    
    # 2. Evaluate Node 1 (TextBlob)
    node_1_score = 0.0
    w1 = 0.0
    if node_1_result:
        node_1_score = node_1_result.get('polarity', 0.0)
        w1 = 0.6 
    
    # 3. Evaluate Node 2 & Insights
    # Logic handled in apply_dynamic_biases
    
    # 4. Generate Composite Score
    w_context = 1.0 if w1 == 0 else 0.4
    raw_score = (node_1_score * w1) + (context_score * w_context)
    
    # 5. Apply Dynamic Biases
    final_score = apply_dynamic_biases(raw_score, node_2_result, engine)
    
    # 6. Classification
    category = get_sentiment_category(final_score, is_sarcastic, pos_count, neg_count, is_factual)
    
    # 7. Learn & Store (Parallel task conceptually)
    engine.track_interaction(
        user_text=text,
        sentiment_category=category,
        node_1_score=node_1_score,
        node_2_prediction=node_2_result.get('prediction'),
        final_score=final_score
    )
    
    # 8. Output
    color = COLORS.get(category, COLORS['RESET'])
    
    return {
        'composite_score': final_score,
        'category': category,
        'color_code': color,
        'is_sarcastic': is_sarcastic,
        'node_2_prediction': node_2_result.get('prediction'),
        'description': f"Score: {final_score:.2f} ({category})"
    }
