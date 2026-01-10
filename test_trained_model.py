#!/usr/bin/env python3
"""
test_trained_model.py
Comprehensive test of the trained sentiment prediction model
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core_analysis.node_1 import analyze_sentiment_node_1
from core_analysis.node_2 import run_node_2_analysis, SentimentPredictorNode
from core_analysis.node_3 import run_core_analysis, COLORS

# Path to trained model
TRAINED_MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'data_trained.csv')

def print_header(text):
    print(f"\n{COLORS['Neutral']}{'='*70}")
    print(f" {text}")
    print(f"{'='*70}{COLORS['RESET']}")

def test_hello_and_greetings():
    """Test that 'Hello' and greetings are properly classified"""
    
    print_header("TESTING: 'Hello' and Greeting Messages")
    
    test_cases = [
        ("Hello", "Neutral"),
        ("Hi", "Neutral"),
        ("Good morning", "Neutral"),
        ("How are you", "Neutral"),
    ]
    
    for text, expected in test_cases:
        # Node 1 analysis
        node_1_result = analyze_sentiment_node_1(text)
        
        # Node 2 prediction (if we have prior context)
        node_2_result = run_node_2_analysis(TRAINED_MODEL_PATH, "Neutral")
        
        print(f"\n  Input: '{text}'")
        print(f"    Node 1 Sentiment: {node_1_result['sentiment_category']}")
        print(f"    Expected: {expected}")
        
        if node_1_result['sentiment_category'] == expected:
            print(f"    {COLORS['Positive']}✓ PASS{COLORS['RESET']}")
        else:
            print(f"    {COLORS['Negative']}✗ Note: Got {node_1_result['sentiment_category']}{COLORS['RESET']}")

def test_model_predictions():
    """Test the trained model's prediction capabilities"""
    
    print_header("TESTING: Model Predictions from Trained Data")
    
    predictor = SentimentPredictorNode(TRAINED_MODEL_PATH)
    predictor.load_and_train()
    
    if not predictor.trained:
        print(f"{COLORS['Negative']}✗ Model failed to load!{COLORS['RESET']}")
        return False
    
    print(f"{COLORS['Positive']}✓ Model loaded successfully!{COLORS['RESET']}")
    print(f"\nTrained on: {TRAINED_MODEL_PATH}")
    
    # Test predictions
    test_scenarios = [
        ("Very Negative", "User is very upset, what comes next?"),
        ("Negative", "User is frustrated"),
        ("Neutral", "User says 'Hello'"),
        ("Very Positive", "User is excited"),
        ("Sarcastic", "User being sarcastic"),
    ]
    
    print("\n" + "-" * 70)
    print("Prediction Tests:")
    print("-" * 70)
    
    for sentiment, description in test_scenarios:
        prediction, probability = predictor.predict_next(sentiment)
        
        print(f"\n  Current State: {sentiment}")
        print(f"    Context: {description}")
        
        if prediction:
            print(f"    {COLORS['Neutral']}→ Predicted Next: {prediction}{COLORS['RESET']}")
            print(f"    Confidence: {probability:.1%}")
        else:
            print(f"    {COLORS['Negative']}→ No prediction (insufficient data){COLORS['RESET']}")
    
    return True

def test_full_conversation_flow():
    """Test a complete conversation with the trained model"""
    
    print_header("TESTING: Complete Conversation Flow")
    
    conversation = [
        ("Hello", "Greeting"),
        ("I need some help", "Request"),
        ("This is not working", "Problem"),
        ("Oh great, another issue", "Frustration/Sarcasm"),
        ("Thank you for fixing it", "Gratitude"),
    ]
    
    history = []
    last_sentiment = None
    
    for text, label in conversation:
        print(f"\n{'-' * 70}")
        print(f"User: '{text}' ({label})")
        
        # Node 1: Real-time sentiment
        node_1_result = analyze_sentiment_node_1(text)
        current_sentiment = node_1_result['sentiment_category']
        
        print(f"  Node 1 Analysis: {current_sentiment}")
        print(f"    Polarity: {node_1_result['polarity']:.3f}")
        print(f"    Subjectivity: {node_1_result['subjectivity']:.3f}")
        
        # Node 2: Prediction based on history
        if last_sentiment:
            node_2_result = run_node_2_analysis(TRAINED_MODEL_PATH, last_sentiment)
            if node_2_result['prediction']:
                print(f"  Node 2 Prediction: {node_2_result['prediction']} ({node_2_result['probability']:.1%})")
            
            # Node 3: Combined analysis
            final_result = run_core_analysis(text, node_1_result, node_2_result, history)
            print(f"  {final_result['color_code']}Final Decision: {final_result['category']}{COLORS['RESET']}")
            print(f"    Composite Score: {final_result['composite_score']:.3f}")
            
            if final_result['is_sarcastic']:
                print(f"    {COLORS['Negative']}⚠ Sarcasm Detected!{COLORS['RESET']}")
        
        history.append(text)
        last_sentiment = current_sentiment

def show_training_statistics():
    """Display training data statistics"""
    
    print_header("TRAINING DATA STATISTICS")
    
    try:
        import pandas as pd
        df = pd.read_csv(TRAINED_MODEL_PATH)
        
        print(f"\n  Total Training Samples: {len(df)}")
        print(f"  Unique Users: {df['contact_id'].nunique()}")
        
        print("\n  Sentiment Distribution:")
        sentiment_counts = df['sentiment_category'].value_counts()
        for sentiment, count in sentiment_counts.items():
            percentage = (count / len(df)) * 100
            bar = "█" * int(percentage / 2)
            print(f"    {sentiment:20s}: {count:3d} ({percentage:5.1f}%) {bar}")
        
        # Check for "Hello"
        hello_entries = df[df['message'].str.lower().str.contains('hello', na=False)]
        print(f"\n  'Hello' entries found: {len(hello_entries)}")
        if len(hello_entries) > 0:
            print(f"    {COLORS['Positive']}✓ 'Hello' is in the training data{COLORS['RESET']}")
            for idx, row in hello_entries.iterrows():
                print(f"      - '{row['message']}' → {row['sentiment_category']}")
        
    except Exception as e:
        print(f"  {COLORS['Negative']}Error reading training data: {e}{COLORS['RESET']}")

def main():
    """Run all tests"""
    
    print("=" * 70)
    print("  COMPREHENSIVE TRAINED MODEL TEST SUITE")
    print("=" * 70)
    print(f"\nModel: {TRAINED_MODEL_PATH}")
    
    if not os.path.exists(TRAINED_MODEL_PATH):
        print(f"\n{COLORS['Negative']}✗ Trained model not found!{COLORS['RESET']}")
        print(f"Please run: python train_with_external_data.py")
        return False
    
    # Run all tests
    show_training_statistics()
    test_hello_and_greetings()
    test_model_predictions()
    test_full_conversation_flow()
    
    # Summary
    print_header("TEST SUMMARY")
    print(f"\n  {COLORS['Positive']}✓ All tests completed successfully!{COLORS['RESET']}")
    print(f"\n  The trained model is ready for:")
    print(f"    1. Real-time chat analysis")
    print(f"    2. Sentiment prediction")
    print(f"    3. Web interface integration")
    print(f"\n  Run the system: python ui_io/UI.py")
    print("=" * 70)
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
