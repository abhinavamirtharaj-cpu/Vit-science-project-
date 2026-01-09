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
from get_resource_path import get_resource_path
TRAIN_DATASET_PATH = get_resource_path('models/train_df.csv')
TEST_DATASET_PATH = get_resource_path('models/test_df.csv')
VAL_DATASET_PATH = get_resource_path('models/val_df.csv')

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
    print_header("TRAINING, TESTING & VALIDATION SUITE")
    print(f"Train Dataset: {TRAIN_DATASET_PATH}")
    print(f"Test Dataset: {TEST_DATASET_PATH}")
    print(f"Validation Dataset: {VAL_DATASET_PATH}")

    for dataset_path, label in [
        (TRAIN_DATASET_PATH, "TRAINING"),
        (TEST_DATASET_PATH, "TEST"),
        (VAL_DATASET_PATH, "VALIDATION")
    ]:
        if not os.path.exists(dataset_path):
            print(f"{COLORS['Negative']}Error: {label} dataset not found!{COLORS['RESET']}")
        else:
            print(f"{COLORS['Positive']}{label} dataset found: {dataset_path}{COLORS['RESET']}")

    # Example: Run test_prediction on each dataset (customize as needed)
    for dataset_path, label in [
        (TRAIN_DATASET_PATH, "TRAINING"),
        (TEST_DATASET_PATH, "TEST"),
        (VAL_DATASET_PATH, "VALIDATION")
    ]:
        print_header(f"{label} DATASET TESTS")
        if os.path.exists(dataset_path):
            test_prediction(
                f"{label} - Sarcasm Prediction Loop",
                last_sentiment="Very Negative",
                user_input="Oh fantastic job breaking it further",
                expected_prediction="Sarcastic"
            )
            test_prediction(
                f"{label} - Post-Sarcasm Volatility",
                last_sentiment="Sarcastic",
                user_input="I am done with this",
                expected_prediction="Very Negative"
            )
            test_prediction(
                f"{label} - Positive Reinforcement",
                last_sentiment="Very Positive",
                user_input="Still loving it",
                expected_prediction="Very Positive"
            )
            test_prediction(
                f"{label} - Neutral Uncertainty",
                last_sentiment="Neutral",
                user_input="It's not working right",
                expected_prediction=None
            )

    print_header("TEST COMPLETED")

if __name__ == "__main__":
    main()
