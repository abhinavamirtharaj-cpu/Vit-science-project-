"""
node_2.py
Data Science Algorithm Node (Prediction).

This node reads sentiment scores from the CSV file, processes historical data,
and predicts the next possible sentiment based on patterns (Markov Chain approach).
"""

import csv
import os
from collections import defaultdict

class SentimentPredictorNode:
    def __init__(self, csv_path):
        self.csv_path = csv_path
        # Use models/train_df.csv for training, models/test_df.csv for testing, models/val_df.csv for validation
        self.training_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models', 'train_df.csv')
        self.test_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models', 'test_df.csv')
        self.val_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models', 'val_df.csv')
        if not os.path.exists(self.training_path):
            self.training_path = csv_path
            
        self.transitions = defaultdict(lambda: defaultdict(int))
        self.totals = defaultdict(int)
        self.trained = False

    def load_and_train(self):
        """Reads sentiment scores from the training CSV file and builds the model."""
        from get_resource_path import get_resource_path
        target_path = get_resource_path(os.path.join('models', os.path.basename(self.training_path)))
        if not os.path.exists(target_path):
            print(f"Warning: Training file not found at {target_path}")
            return

        try:
            with open(target_path, 'r', newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                # Group messages by contact to analyze individual flows
                user_flows = defaultdict(list)
                for row in reader:
                    # We are interested in the flow of sentiments. 
                    # We can track 'sent' (user) messages.
                    if row.get('dir') == 'sent' and row.get('sentiment_category'):
                        contact_id = row.get('contact_id')
                        sentiment = row.get('sentiment_category')
                        user_flows[contact_id].append(sentiment)
                
                # Build transitions
                for sentiments in user_flows.values():
                    for i in range(len(sentiments) - 1):
                        current_s = sentiments[i]
                        next_s = sentiments[i+1]
                        self.transitions[current_s][next_s] += 1
                        self.totals[current_s] += 1
            
            self.trained = True
            # print(f"DEBUG: Node 2 trained on {target_path}")
            
        except Exception as e:
            print(f"Error reading CSV file: {e}")

    def predict_next(self, current_sentiment):
        """
        Predicts the next possible sentiment based on patterns.
        """
        if not self.trained:
            self.load_and_train()

        if current_sentiment not in self.transitions:
            return None, 0.0

        possible_next = self.transitions[current_sentiment]
        total = self.totals[current_sentiment]

        if total == 0:
            return None, 0.0

        # Find most likely next state
        best_next = None
        max_count = -1
        
        for sentiment, count in possible_next.items():
            if count > max_count:
                max_count = count
                best_next = sentiment
        
        probability = max_count / total
        return best_next, probability

def run_node_2_analysis(csv_path, current_sentiment):
    """
    Main entry point for Node 2.
    """
    predictor = SentimentPredictorNode(csv_path)
    predictor.load_and_train()
    prediction, probability = predictor.predict_next(current_sentiment)
    
    return {
        'prediction': prediction,
        'probability': probability,
        'source': 'node_2'
    }
