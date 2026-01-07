"""
run_ds_demo.py
Demonstration script for the Data Science Algorithm (Nodes 2 & 3) 
using a pragmatic, realistic dataset.
"""

import sys
import os
import time

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core_analysis.node_1 import analyze_sentiment_node_1
from core_analysis.node_2 import run_node_2_analysis
from core_analysis.node_3 import run_core_analysis, COLORS

# Path to our new pragmatic dataset
DATASET_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ui_io', 'pragmatic_dataset.csv')

def print_section(title):
    print(f"\n{COLORS['Neutral']}{'='*60}")
    print(f"{title}")
    print(f"{'='*60}{COLORS['RESET']}")

def run_demo_step(step_name, user_input, last_sentiment_context, history_context):
    print(f"\n{COLORS['Positive']}--- {step_name} ---{COLORS['RESET']}")
    print(f"User Input: '{user_input}'")
    print(f"Context (Last Sentiment): {last_sentiment_context}")
    
    # 1. Run Node 2 (Prediction based on history patterns)
    print(f"{COLORS['Neutral']}Running Node 2 (Prediction)...{COLORS['RESET']}")
    node_2_result = run_node_2_analysis(DATASET_PATH, last_sentiment_context)
    print(f"  -> Prediction: {node_2_result['prediction']} (Prob: {node_2_result['probability']:.2f})")

    # 2. Run Node 1 (Placeholder)
    node_1_result = analyze_sentiment_node_1(user_input)

    # 3. Run Node 3 (Core Analysis & Decision)
    print(f"{COLORS['Neutral']}Running Node 3 (Core Analysis)...{COLORS['RESET']}")
    final_result = run_core_analysis(user_input, node_1_result, node_2_result, history_context)

    # Display Result
    category = final_result['category']
    score = final_result['composite_score']
    color = final_result['color_code']
    is_sarcastic = final_result['is_sarcastic']

    print(f"\n{color}FINAL RESULT:")
    print(f"  Category: {category}")
    print(f"  Score:    {score:.3f}")
    if is_sarcastic:
        print(f"  [!] Sarcasm Detected")
    print(f"{COLORS['RESET']}")
    return category

def main():
    print_section("Initializing DS Algorithm Demo with Pragmatic Dataset")
    print(f"Dataset: {DATASET_PATH}")
    
    if not os.path.exists(DATASET_PATH):
        print(f"{COLORS['Negative']}Error: Dataset not found!{COLORS['RESET']}")
        return

    # Mock History Context (simulating what would be read from the file)
    # We'll use a subset of the texts from our CSV for context analysis
    mock_history = [
        "Hello there", "I am having a serious issue", "It has been delayed", 
        "Okay I understand", "Thanks for explaining", "My package arrived damaged"
    ]

    # --- Scenario 1: User is currently Negative (e.g., after "My package arrived damaged") ---
    # In our dataset, "Very Negative" (damaged package) was followed by "Sarcastic" ("Great, just what I needed").
    # Let's see if Node 2 predicts Sarcastic or Negative patterns.
    # Note: Our CSV has: Very Negative -> Sarcastic.
    
    last_sentiment = "Very Negative"
    current_input = "This is absolutely brilliant, thanks a lot for breaking it." # Sarcastic input
    
    run_demo_step("Scenario 1: Predicting after Negative Event", 
                  current_input, 
                  last_sentiment, 
                  mock_history)

    # --- Scenario 2: User is Neutral/Calming down ---
    # In dataset: Neutral -> Positive.
    last_sentiment = "Neutral"
    current_input = "I appreciate the help."
    
    run_demo_step("Scenario 2: Predicting after Neutral State", 
                  current_input, 
                  last_sentiment, 
                  mock_history)

    # --- Scenario 3: Alice (user_real_001) vs Bob (user_real_002) Patterns ---
    # Bob is always Very Positive.
    # If we feed "Very Positive", Node 2 should predict "Very Positive" with high probability.
    
    last_sentiment = "Very Positive"
    current_input = "Another great feature!"
    
    run_demo_step("Scenario 3: Strong Positive Pattern (Bob's Style)", 
                  current_input, 
                  last_sentiment, 
                  mock_history)

    print_section("Demo Completed")

if __name__ == "__main__":
    main()
