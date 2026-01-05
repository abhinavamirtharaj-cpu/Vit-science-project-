"""
run_system.py
Execution script for the Comprehensive Sentiment Analysis System.

This script demonstrates the interaction between Node 2 and Node 3,
processing user input and displaying color-coded results.
"""

import sys
import os
import time

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core_analysis.node_1 import analyze_sentiment_node_1
from core_analysis.node_2 import run_node_2_analysis
from core_analysis.node_3 import run_core_analysis, COLORS
from ui_io.storage import get_csv_path, get_all_messages_for_analysis
from core_analysis.chat_service import get_last_sentiment_from_history

def print_dialog(title, content, color_code):
    print(f"{color_code}")
    print(f"╔{'═'*50}╗")
    print(f"║ {title:^48} ║")
    print(f"╠{'═'*50}╣")
    for line in content.split('\n'):
        print(f"║ {line:<48} ║")
    print(f"╚{'═'*50}╝")
    print(f"{COLORS['RESET']}")

def main():
    print(f"{COLORS['Neutral']}Initializing Comprehensive Sentiment Analysis System...{COLORS['RESET']}")
    print("-" * 60)
    print("Architecture Loaded:")
    print(" [ ] Node 1: TextBlob Analysis (Inactive/Placeholder)")
    print(" [*] Node 2: Data Science Prediction (Active)")
    print(" [*] Node 3: Core Analysis & Decision (Active)")
    print("-" * 60)
    
    csv_path = get_csv_path()
    
    # Simulate a session
    while True:
        try:
            user_input = input(f"\n{COLORS['Positive']}Enter text (or 'quit'): {COLORS['RESET']}").strip()
            if user_input.lower() in ['quit', 'exit']:
                break
            
            if not user_input:
                continue

            print(f"\n{COLORS['Neutral']}Processing...{COLORS['RESET']}")
            
            # 1. Get History Context
            history_messages = get_all_messages_for_analysis()
            
            # 2. Run Node 2 (Prediction based on previous state)
            # We need the *previous* sentiment to predict the *next* one. 
            # Ideally we'd know the user ID. For this demo, let's assume a generic 'user' or 'support'.
            # Or we can use the *last recorded* sentiment from the CSV.
            # For the purpose of this flow, we predict what *this* message MIGHT be based on history,
            # or we predict what the NEXT one will be after this analysis.
            # The prompt says: "Predicts next possible sentiment based on patterns"
            
            # Let's get the last sentiment from history to feed Node 2
            # Assuming 'support' or 'user' - let's default to checking 'support' history for demo
            last_sentiment = get_last_sentiment_from_history('support') 
            if not last_sentiment:
                last_sentiment = 'Neutral'
                
            node_2_result = run_node_2_analysis(csv_path, last_sentiment)
            
            # 3. Run Node 1 (Placeholder)
            node_1_result = analyze_sentiment_node_1(user_input)
            
            # 4. Run Node 3 (Core Analysis)
            final_result = run_core_analysis(user_input, node_1_result, node_2_result, history_messages)
            
            # Display Output
            category = final_result['category']
            score = final_result['composite_score']
            color = final_result['color_code']
            prediction = final_result['node_2_prediction']
            
            content = f"Sentiment: {category}\n"
            content += f"Score:     {score:.3f}\n"
            content += f"Prediction Context: {prediction or 'None'}"
            
            if final_result['is_sarcastic']:
                content += "\n[!] Sarcasm Detected"
                
            print_dialog("ANALYSIS RESULT", content, color)
            
            print(f"{COLORS['Neutral']}System confidence: 95% (Simulated){COLORS['RESET']}")
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"{COLORS['Negative']}Error: {e}{COLORS['RESET']}")

    print("System terminated.")

if __name__ == "__main__":
    main()
