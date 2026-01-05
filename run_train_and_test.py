"""
run_train_and_test.py
Script to train the Data Science Node (Node 2) with a custom dataset
and verify the results with Node 3.
"""

import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core_analysis.node_1 import analyze_sentiment_node_1
from core_analysis.node_2 import run_node_2_analysis
from core_analysis.node_3 import run_core_analysis, COLORS

# Path to the training dataset
TRAIN_DATASET_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ui_io', 'train.csv')

def print_header(text):
    print(f"\n{COLORS['Neutral']}{'='*60}")
    print(f" {text}")
    print(f"{'='*60}{COLORS['RESET']}")

def test_prediction(test_name, last_sentiment, user_input, expected_prediction=None):
    print(f"\n{COLORS['Positive']}Test Case: {test_name}{COLORS['RESET']}")
    print(f"  Context (Last Sentiment): {last_sentiment}")
    print(f"  User Input: '{user_input}'")

    # 1. Train/Run Node 2
    print(f"  {COLORS['Neutral']}Running Node 2 (Prediction)...{COLORS['RESET']}")
    node_2_result = run_node_2_analysis(TRAIN_DATASET_PATH, last_sentiment)
    prediction = node_2_result['prediction']
    probability = node_2_result['probability']
    
    print(f"  -> Prediction: {prediction} (Confidence: {probability:.2f})")
    
    if expected_prediction:
        if prediction == expected_prediction:
            print(f"     [PASS] Matches expected behavior.")
        else:
            print(f"     [INFO] Prediction differs from hypothesis (Expected: {expected_prediction}).")

    # 2. Run Node 3
    print(f"  {COLORS['Neutral']}Running Node 3 (Core Analysis)...{COLORS['RESET']}")
    # Mock history for context
    mock_history = ["I need help", "It is broken"] 
    
    # Node 1 placeholder
    node_1_result = analyze_sentiment_node_1(user_input)
    
    final_result = run_core_analysis(user_input, node_1_result, node_2_result, mock_history)
    
    print(f"  {final_result['color_code']}FINAL DECISION:{COLORS['RESET']}")
    print(f"    Category: {final_result['category']}")
    print(f"    Score:    {final_result['composite_score']:.3f}")
    if final_result['is_sarcastic']:
        print(f"    [!] Sarcasm Detected")

def main():
    print_header("TRAINING & TESTING SUITE")
    print(f"Dataset: {TRAIN_DATASET_PATH}")
    
    if not os.path.exists(TRAIN_DATASET_PATH):
        print(f"{COLORS['Negative']}Error: Training dataset not found!{COLORS['RESET']}")
        return

    # --- Test 1: Sarcasm Prediction ---
    # In our dataset, 'Very Negative' is often followed by 'Sarcastic' (e.g. user_1, user_5, user_8)
    test_prediction(
        "Sarcasm Prediction Loop",
        last_sentiment="Very Negative",
        user_input="Oh fantastic job breaking it further",
        expected_prediction="Sarcastic"
    )

    # --- Test 2: Recovery Pattern ---
    # 'Sarcastic' is often followed by 'Negative' or 'Very Negative' or 'Neutral' depending on user.
    # In our data: 
    # user_1: Sarcastic -> Very Negative
    # user_5: Sarcastic -> Neutral
    # user_8: Sarcastic -> Very Negative
    # So 'Very Negative' is a likely outcome.
    test_prediction(
        "Post-Sarcasm Volatility",
        last_sentiment="Sarcastic",
        user_input="I am done with this",
        expected_prediction="Very Negative"
    )

    # --- Test 3: Positive Flow ---
    # 'Very Positive' -> 'Very Positive' (user_2, user_7)
    test_prediction(
        "Positive Reinforcement",
        last_sentiment="Very Positive",
        user_input="Still loving it",
        expected_prediction="Very Positive"
    )

    # --- Test 4: Neutral Start ---
    # 'Neutral' -> 'Negative' (user_1, user_3) or 'Positive' (user_6)
    # It's split. Let's see what the probability says.
    test_prediction(
        "Neutral Uncertainty",
        last_sentiment="Neutral",
        user_input="It's not working right",
        expected_prediction=None 
    )

    print_header("TEST COMPLETED")

if __name__ == "__main__":
    main()
