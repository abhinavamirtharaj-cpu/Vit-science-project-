"""
node_ds.py - Data Structure and Algorithm for Sentiment Prediction

This module implements a Markov Chain-based prediction model using a linked list structure (Node).
It reads chat history from the CSV file, builds a transition matrix of sentiments,
and predicts the next probable sentiment based on the user's last sentiment.
"""

import csv
import os
import random
from collections import defaultdict

# Use the existing CSV file path logic from storage.py (conceptually)
# We will pass the CSV path or data to the training function.

class Node:
    """
    A generic Node class for data structures.
    Used here to represent a state in the sentiment chain.
    """
    def __init__(self, data=None):
        self.data = data  # Sentiment category (e.g., "Very Positive")
        self.next = None  # Pointer to next node (not strictly used in dict-graph but kept for DS structure)

    def __repr__(self):
        return f"Node({self.data})"

class SentimentMarkovChain:
    """
    A simple Markov Chain model to predict the next sentiment.
    It builds a graph where nodes are sentiments and edges are transition probabilities.
    """
    def __init__(self):
        # transitions[current_sentiment][next_sentiment] = count
        self.transitions = defaultdict(lambda: defaultdict(int))
        self.totals = defaultdict(int)

    def train(self, history_data):
        """
        Train the model using the provided chat history.
        history_data: list of dicts containing 'sentiment_category' and 'contact_id'
        """
        # We need to process messages in chronological order per user to find transitions
        # Group messages by contact_id
        user_messages = defaultdict(list)
        for msg in history_data:
            c_id = msg.get('contact_id')
            # Only consider 'sent' messages (user's own sentiment flow) or mix? 
            # The prompt asks for "sentiment of the end user alone".
            # Assuming 'dir' == 'sent' is the user we want to predict for (the one typing).
            if c_id and msg.get('dir') == 'sent':
                # Parse date to ensure order if not already sorted? 
                # CSV is usually append-only, so we assume file order is chronological.
                sent_cat = msg.get('sentiment_category')
                if sent_cat: # Filter out empty sentiments
                    user_messages[c_id].append(sent_cat)

        # Build transitions
        for user, sentiments in user_messages.items():
            for i in range(len(sentiments) - 1):
                current_s = sentiments[i]
                next_s = sentiments[i+1]
                
                self.transitions[current_s][next_s] += 1
                self.totals[current_s] += 1

    def predict_next(self, current_sentiment):
        """
        Predict the next probable sentiment based on the current one.
        Returns a tuple (predicted_sentiment, probability).
        """
        if current_sentiment not in self.transitions:
            return None, 0.0

        possible_next = self.transitions[current_sentiment]
        total_occurrences = self.totals[current_sentiment]

        if total_occurrences == 0:
            return None, 0.0

        # Find the most frequent next sentiment
        best_next = None
        max_count = -1

        for sentiment, count in possible_next.items():
            if count > max_count:
                max_count = count
                best_next = sentiment
        
        probability = max_count / total_occurrences
        return best_next, probability

    def get_transition_matrix(self):
        """
        Returns the transition probabilities for inspection.
        """
        matrix = {}
        for start_node, next_nodes in self.transitions.items():
            total = self.totals[start_node]
            probs = {k: v / total for k, v in next_nodes.items()}
            matrix[start_node] = probs
        return matrix

def load_data_and_train(csv_path):
    """
    Reads the CSV file and trains the Markov Chain model.
    """
    history = []
    if os.path.exists(csv_path):
        with open(csv_path, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                history.append(row)
    
    model = SentimentMarkovChain()
    model.train(history)
    return model

# Global instance (can be refreshed)
_model_instance = None

def get_prediction(current_sentiment, csv_path):
    """
    Main entry point to get a prediction.
    Reloads data to ensure "ML-like" continuous learning from new data.
    """
    global _model_instance
    # Re-train every time to simulate "learning on the data we give"
    _model_instance = load_data_and_train(csv_path)
    
    prediction, prob = _model_instance.predict_next(current_sentiment)
    return prediction, prob
