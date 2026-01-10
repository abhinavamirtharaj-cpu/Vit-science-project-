#!/usr/bin/env python3
"""
train_with_external_data.py
Complete training pipeline for external emotion/sentiment datasets
"""

import os
import sys
import pandas as pd
from preprocess_training_data import (
    process_conversation_text,
    process_emotion_dataset,
    process_test_data,
    process_tsv_multilabel,
    process_data_csv,
    process_final_dataset,
    process_data_txt,
    process_emotion_classify,
    process_text_emotion,
    process_emotion_tweets,
    process_test_predictions,
    process_eng_csv,
    consolidate_all_datasets,
    EMOTION_TO_SENTIMENT
)

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core_analysis.node_2 import run_node_2_analysis, SentimentPredictorNode
from core_analysis.node_3 import run_core_analysis, COLORS

def find_external_files():
    """
    Locate external CSV files in various possible locations
    """
    possible_base_paths = [
        '/workspaces/SCIVIT-Draft/training_data',
        '/tmp',
        os.path.expanduser('~'),
        '/workspaces',
        '/root',
        os.getcwd(),
    ]
    
    file_names = [
        'conversation_text.csv',
        'emotion_dataset_v5_clean.csv',
        'Test_Data.csv',
        'test.tsv',
        'data.csv',
        'final_dataset (1).csv',
        'DATA.txt',
        'Emotion_classify_Data.csv',
        'text_emotion.csv',
        'text_emotion (1).csv',
        'emotion_tweets.csv',
        'test_predictions_full.csv',
        'eng.csv',
        # Also accept any CSV with these column patterns
        '*.csv',
        '*.tsv',
        '*.txt',
    ]
    
    file_mappings = {}
    processor_mappings = {
        'conversation_text.csv': process_conversation_text,
        'emotion_dataset_v5_clean.csv': process_emotion_dataset,
        'Test_Data.csv': process_test_data,
        'test.tsv': process_tsv_multilabel,
        'data.csv': process_data_csv,
        'final_dataset (1).csv': process_final_dataset,
        'DATA.txt': process_data_txt,
        'Emotion_classify_Data.csv': process_emotion_classify,
        'text_emotion.csv': process_text_emotion,
        'text_emotion (1).csv': process_text_emotion,
        'emotion_tweets.csv': process_emotion_tweets,
        'test_predictions_full.csv': process_test_predictions,
        'eng.csv': process_eng_csv,
    }
    
    print("\n🔍 Searching for training files...")
    
    # First, try exact matches
    for filename in file_names:
        if filename.startswith('*'):
            continue
        for base_path in possible_base_paths:
            full_path = os.path.join(base_path, filename)
            if os.path.exists(full_path) and full_path not in file_mappings:
                file_mappings[full_path] = processor_mappings.get(filename)
                print(f"  ✓ Found: {filename}")
                break
    
    # Then, scan directories for any CSV/TSV files and auto-detect
    for base_path in possible_base_paths:
        if not os.path.exists(base_path) or not os.path.isdir(base_path):
            continue
        try:
            for file in os.listdir(base_path):
                if not file.endswith(('.csv', '.tsv', '.txt')):
                    continue
                full_path = os.path.join(base_path, file)
                if full_path in file_mappings:
                    continue  # Already processed
                
                # Check if filename matches any pattern
                matched = False
                for pattern, processor in processor_mappings.items():
                    if pattern in file:
                        file_mappings[full_path] = processor
                        print(f"  ✓ Found: {file}")
                        matched = True
                        break
                
                # Try auto-detection for unknown files
                if not matched:
                    processor = auto_detect_format(full_path)
                    if processor:
                        file_mappings[full_path] = processor
                        print(f"  ✓ Found (auto-detected): {file}")
        except PermissionError:
            continue
    
    return file_mappings

def auto_detect_format(filepath):
    """Auto-detect CSV format and return appropriate processor"""
    try:
        import pandas as pd
        
        # Read first few rows
        if filepath.endswith('.tsv'):
            df = pd.read_csv(filepath, sep='\t', nrows=3)
        elif filepath.endswith('.txt'):
            # Check if it's semicolon-separated
            with open(filepath, 'r') as f:
                first_line = f.readline()
                if ';' in first_line:
                    return process_data_txt
            return None
        else:
            df = pd.read_csv(filepath, nrows=3)
        
        columns = [col.lower() for col in df.columns]
        
        # Detect based on column names
        if 'emotion_label' in columns and 'text' in columns:
            return process_conversation_text
        elif 'emotion' in columns and ('sentence' in columns or 'cleaned_text' in columns):
            return process_emotion_dataset
        elif 'subtitle' in columns and 'emotion' in columns:
            return process_test_data
        elif any(emotion in columns for emotion in ['joy', 'fear', 'anger', 'sadness']):
            # Multi-label format
            if filepath.endswith('.tsv') or 'Surprise' in df.columns or 'Disgust' in df.columns:
                return process_tsv_multilabel
            else:
                return process_eng_csv
        elif 'labels' in columns and 'text' in columns:
            return process_data_csv
        elif 'emotion' in columns and 'text' in columns:
            return process_final_dataset
        elif 'comment' in columns and 'emotion' in columns:
            return process_emotion_classify
        elif 'sentiment' in columns and ('content' in columns or 'author' in columns):
            return process_text_emotion
        elif 'tweet' in columns and 'emotion' in columns:
            return process_emotion_tweets
        elif 'sentiment_category' in columns:
            return process_test_predictions
        
        return None
    except Exception as e:
        return None

def train_model(consolidated_df, output_path):
    """Train the sentiment prediction model"""
    
    print("\n" + "=" * 60)
    print("TRAINING SENTIMENT PREDICTION MODEL")
    print("=" * 60)
    
    # Save to training location
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    consolidated_df.to_csv(output_path, index=False)
    print(f"✓ Training data saved to: {output_path}")
    
    # Initialize and train the predictor
    predictor = SentimentPredictorNode(output_path)
    predictor.load_and_train()
    
    if predictor.trained:
        print("✓ Model successfully trained!")
        
        # Show transition statistics
        print("\n📊 Learned Sentiment Transitions:")
        for current_sent, transitions in predictor.transitions.items():
            if transitions:
                print(f"\n  From '{current_sent}':")
                total = predictor.totals[current_sent]
                for next_sent, count in sorted(transitions.items(), key=lambda x: x[1], reverse=True)[:3]:
                    prob = (count / total) * 100
                    print(f"    → {next_sent:20s} ({prob:5.1f}% probability)")
        
        return predictor
    else:
        print("✗ Model training failed!")
        return None

def test_model(predictor):
    """Test the trained model with sample predictions"""
    
    print("\n" + "=" * 60)
    print("TESTING MODEL PREDICTIONS")
    print("=" * 60)
    
    test_cases = [
        ("Very Negative", "This is terrible"),
        ("Negative", "I'm not happy about this"),
        ("Neutral", "Okay, let's see"),
        ("Positive", "That's pretty good"),
        ("Very Positive", "I absolutely love this!"),
    ]
    
    for current_sentiment, example_text in test_cases:
        prediction, probability = predictor.predict_next(current_sentiment)
        
        print(f"\n  Given: '{current_sentiment}'")
        print(f"    Example: \"{example_text}\"")
        if prediction:
            print(f"    Predicted Next: {prediction} ({probability:.1%} confidence)")
        else:
            print(f"    Predicted Next: (No data for this transition)")

def main():
    """Main execution pipeline"""
    
    print("=" * 60)
    print("MULTI-DATASET EMOTION SENTIMENT TRAINING PIPELINE")
    print("=" * 60)
    
    # Step 1: Locate external files
    file_mappings = find_external_files()
    
    if not file_mappings:
        print("\n" + "=" * 60)
        print("⚠ NO TRAINING FILES FOUND")
        print("=" * 60)
        print("\nPlease provide CSV files by:")
        print("1. Copying them to /tmp/ directory")
        print("2. Or placing them in the current directory")
        print("\nSupported file formats:")
        print("  - conversation_text.csv")
        print("  - emotion_dataset_v5_clean.csv")
        print("  - Test_Data.csv")
        print("  - test.tsv")
        print("  - data.csv")
        print("  - final_dataset (1).csv")
        print("  - DATA.txt")
        print("  - Emotion_classify_Data.csv")
        print("  - text_emotion.csv")
        print("  - emotion_tweets.csv")
        print("  - test_predictions_full.csv")
        print("  - eng.csv")
        print("=" * 60)
        return False
    
    print(f"\n✓ Found {len(file_mappings)} training files")
    
    # Step 2: Process and consolidate datasets
    consolidated_df = consolidate_all_datasets(file_mappings)
    
    if consolidated_df is None or consolidated_df.empty:
        print("\n❌ Failed to consolidate training data")
        return False
    
    # Step 3: Train the model
    output_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'data',
        'data_trained.csv'
    )
    
    predictor = train_model(consolidated_df, output_path)
    
    if predictor is None:
        return False
    
    # Step 4: Test the model
    test_model(predictor)
    
    print("\n" + "=" * 60)
    print("✓ TRAINING COMPLETE!")
    print("=" * 60)
    print("\nThe model is now ready to use. You can:")
    print("  1. Run the main system: python run_system.py")
    print("  2. Test predictions: python run_train_and_test.py")
    print("  3. Use in web interface: python ui_io/UI.py")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
