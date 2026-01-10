"""
preprocess_training_data.py
Universal data preprocessor for multiple emotion/sentiment datasets.
Converts various formats into the unified training format expected by Node 2.
"""

import pandas as pd
import os
from collections import defaultdict

# Emotion to Sentiment Category Mapping
EMOTION_TO_SENTIMENT = {
    # Positive emotions
    'joy': 'Very Positive',
    'happiness': 'Very Positive',
    'love': 'Very Positive',
    'excitement': 'Positive',
    'enthusiasm': 'Positive',
    'fun': 'Positive',
    'admiration': 'Positive',
    'amusement': 'Positive',
    'approval': 'Positive',
    'caring': 'Positive',
    'gratitude': 'Positive',
    'relief': 'Positive',
    'pride': 'Positive',
    'optimism': 'Positive',
    
    # Neutral emotions
    'neutral': 'Neutral',
    'surprise': 'Neutral',
    'realization': 'Neutral',
    'confusion': 'Neutral',
    'curiosity': 'Neutral',
    
    # Negative emotions
    'anger': 'Negative',
    'annoyance': 'Negative',
    'disapproval': 'Negative',
    'sadness': 'Very Negative',
    'fear': 'Very Negative',
    'worry': 'Negative',
    'hate': 'Very Negative',
    'grief': 'Very Negative',
    'nervousness': 'Negative',
    'disgust': 'Negative',
    'disappointment': 'Negative',
    'embarrassment': 'Negative',
    'shame': 'Very Negative',
    'guilt': 'Negative',
    'remorse': 'Negative',
    
    # Sarcastic (detected through context)
    'sarcasm': 'Sarcastic',
    'sarcastic': 'Sarcastic',
    
    # Numeric sentiment (for data.csv)
    '0': 'Very Positive',  # Joy
    '1': 'Negative',       # Anger
    '2': 'Very Negative',  # Fear
    '3': 'Very Negative',  # Sadness
    '4': 'Neutral',        # Surprise
    '5': 'Negative',       # Disgust
    '6': 'Positive',       # Excitement
    '7': 'Neutral',        # Neutral/Informative
}

def process_conversation_text(filepath):
    """Process conversation_text.csv with emotion_label column"""
    try:
        df = pd.read_csv(filepath)
        processed = []
        
        for idx, row in df.iterrows():
            emotion = str(row.get('emotion_label', 'neutral')).lower()
            text = row.get('text', '')
            conversation_id = row.get('conversation_id', 0)
            
            sentiment = EMOTION_TO_SENTIMENT.get(emotion, 'Neutral')
            processed.append({
                'contact_id': f'user_{conversation_id}',
                'message': text,
                'dir': 'sent',
                'sentiment_category': sentiment
            })
        
        return pd.DataFrame(processed)
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return pd.DataFrame()

def process_emotion_dataset(filepath):
    """Process emotion_dataset_v5_clean.csv with sentence,emotion columns"""
    try:
        df = pd.read_csv(filepath)
        processed = []
        
        for idx, row in df.iterrows():
            emotion = str(row.get('emotion', 'neutral')).lower()
            text = row.get('sentence', row.get('cleaned_text', ''))
            
            sentiment = EMOTION_TO_SENTIMENT.get(emotion, 'Neutral')
            processed.append({
                'contact_id': f'user_{idx % 100}',  # Distribute across 100 users
                'message': text,
                'dir': 'sent',
                'sentiment_category': sentiment
            })
        
        return pd.DataFrame(processed)
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return pd.DataFrame()

def process_test_data(filepath):
    """Process Test_Data.csv with Subtitle,Emotion columns"""
    try:
        df = pd.read_csv(filepath)
        processed = []
        
        for idx, row in df.iterrows():
            emotion = str(row.get('Emotion', 'neutral')).lower()
            text = row.get('Subtitle', '')
            
            sentiment = EMOTION_TO_SENTIMENT.get(emotion, 'Neutral')
            processed.append({
                'contact_id': f'user_{idx % 50}',
                'message': text,
                'dir': 'sent',
                'sentiment_category': sentiment
            })
        
        return pd.DataFrame(processed)
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return pd.DataFrame()

def process_tsv_multilabel(filepath):
    """Process test.tsv with multi-label emotions"""
    try:
        df = pd.read_csv(filepath, sep='\t')
        processed = []
        
        emotion_cols = ['Joy', 'Fear', 'Anger', 'Sadness', 'Disgust', 'Surprise']
        
        for idx, row in df.iterrows():
            text = row.get('text', '')
            
            # Find dominant emotion
            max_score = 0
            dominant_emotion = 'neutral'
            
            for col in emotion_cols:
                if col in row and row[col] > max_score:
                    max_score = row[col]
                    dominant_emotion = col.lower()
            
            sentiment = EMOTION_TO_SENTIMENT.get(dominant_emotion, 'Neutral')
            processed.append({
                'contact_id': f'user_{idx % 75}',
                'message': text,
                'dir': 'sent',
                'sentiment_category': sentiment
            })
        
        return pd.DataFrame(processed)
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return pd.DataFrame()

def process_data_csv(filepath):
    """Process data.csv with numeric labels"""
    try:
        df = pd.read_csv(filepath)
        processed = []
        
        for idx, row in df.iterrows():
            text = row.get('text', '')
            label = str(row.get('labels', '7'))
            
            sentiment = EMOTION_TO_SENTIMENT.get(label, 'Neutral')
            processed.append({
                'contact_id': f'user_{idx % 60}',
                'message': text,
                'dir': 'sent',
                'sentiment_category': sentiment
            })
        
        return pd.DataFrame(processed)
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return pd.DataFrame()

def process_final_dataset(filepath):
    """Process final_dataset (1).csv with text,emotion columns"""
    try:
        df = pd.read_csv(filepath)
        processed = []
        
        for idx, row in df.iterrows():
            emotion = str(row.get('emotion', 'neutral')).lower()
            text = row.get('text', '')
            
            sentiment = EMOTION_TO_SENTIMENT.get(emotion, 'Neutral')
            processed.append({
                'contact_id': f'user_{idx % 80}',
                'message': text,
                'dir': 'sent',
                'sentiment_category': sentiment
            })
        
        return pd.DataFrame(processed)
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return pd.DataFrame()

def process_data_txt(filepath):
    """Process DATA.txt with semicolon-separated format"""
    try:
        processed = []
        
        with open(filepath, 'r', encoding='utf-8') as f:
            for idx, line in enumerate(f):
                if ';' in line:
                    parts = line.strip().split(';')
                    if len(parts) >= 2:
                        text = parts[0]
                        emotion = parts[1].lower()
                        
                        sentiment = EMOTION_TO_SENTIMENT.get(emotion, 'Neutral')
                        processed.append({
                            'contact_id': f'user_{idx % 90}',
                            'message': text,
                            'dir': 'sent',
                            'sentiment_category': sentiment
                        })
        
        return pd.DataFrame(processed)
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return pd.DataFrame()

def process_emotion_classify(filepath):
    """Process Emotion_classify_Data.csv with Comment,Emotion columns"""
    try:
        df = pd.read_csv(filepath)
        processed = []
        
        for idx, row in df.iterrows():
            emotion = str(row.get('Emotion', 'neutral')).lower()
            text = row.get('Comment', '')
            
            sentiment = EMOTION_TO_SENTIMENT.get(emotion, 'Neutral')
            processed.append({
                'contact_id': f'user_{idx % 70}',
                'message': text,
                'dir': 'sent',
                'sentiment_category': sentiment
            })
        
        return pd.DataFrame(processed)
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return pd.DataFrame()

def process_text_emotion(filepath):
    """Process text_emotion.csv with tweet content and sentiment"""
    try:
        df = pd.read_csv(filepath)
        processed = []
        
        for idx, row in df.iterrows():
            emotion = str(row.get('sentiment', 'neutral')).lower()
            text = row.get('content', '')
            author = row.get('author', f'user_{idx % 100}')
            
            sentiment = EMOTION_TO_SENTIMENT.get(emotion, 'Neutral')
            processed.append({
                'contact_id': author,
                'message': text,
                'dir': 'sent',
                'sentiment_category': sentiment
            })
        
        return pd.DataFrame(processed)
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return pd.DataFrame()

def process_emotion_tweets(filepath):
    """Process emotion_tweets.csv with Tweet,Emotion columns"""
    try:
        df = pd.read_csv(filepath)
        processed = []
        
        for idx, row in df.iterrows():
            emotion = str(row.get('Emotion', 'neutral')).lower()
            text = row.get('Tweet', '')
            
            sentiment = EMOTION_TO_SENTIMENT.get(emotion, 'Neutral')
            processed.append({
                'contact_id': f'user_{idx % 85}',
                'message': text,
                'dir': 'sent',
                'sentiment_category': sentiment
            })
        
        return pd.DataFrame(processed)
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return pd.DataFrame()

def process_test_predictions(filepath):
    """Process test_predictions_full.csv with sentiment_category column"""
    try:
        df = pd.read_csv(filepath)
        processed = []
        
        for idx, row in df.iterrows():
            sentiment = str(row.get('sentiment_category', 'Neutral'))
            text = row.get('originaltweet', '')
            location = row.get('location', 'Unknown')
            
            # Use location as part of contact_id for geographic patterns
            contact_id = f"{location}_{idx % 50}".replace(' ', '_')
            
            processed.append({
                'contact_id': contact_id,
                'message': text,
                'dir': 'sent',
                'sentiment_category': sentiment
            })
        
        return pd.DataFrame(processed)
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return pd.DataFrame()

def process_eng_csv(filepath):
    """Process eng.csv with multi-label emotion columns"""
    try:
        df = pd.read_csv(filepath)
        processed = []
        
        emotion_cols = ['Anger', 'Fear', 'Joy', 'Sadness', 'Surprise']
        
        for idx, row in df.iterrows():
            text = row.get('text', '')
            
            # Find dominant emotion
            max_score = 0
            dominant_emotion = 'neutral'
            
            for col in emotion_cols:
                if col in row and row[col] > max_score:
                    max_score = row[col]
                    dominant_emotion = col.lower()
            
            sentiment = EMOTION_TO_SENTIMENT.get(dominant_emotion, 'Neutral')
            processed.append({
                'contact_id': f'user_{idx % 65}',
                'message': text,
                'dir': 'sent',
                'sentiment_category': sentiment
            })
        
        return pd.DataFrame(processed)
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return pd.DataFrame()

def consolidate_all_datasets(file_mappings):
    """Process all datasets and consolidate into unified format"""
    
    all_data = []
    
    print("=" * 60)
    print("PROCESSING TRAINING DATA FROM MULTIPLE SOURCES")
    print("=" * 60)
    
    for file_path, processor_func in file_mappings.items():
        if os.path.exists(file_path):
            print(f"\n✓ Processing: {os.path.basename(file_path)}")
            df = processor_func(file_path)
            if not df.empty:
                print(f"  → Extracted {len(df)} samples")
                all_data.append(df)
            else:
                print(f"  ⚠ No data extracted")
        else:
            print(f"\n✗ File not found: {file_path}")
    
    if not all_data:
        print("\n❌ No data could be processed!")
        return None
    
    # Consolidate all dataframes
    consolidated_df = pd.concat(all_data, ignore_index=True)
    
    # Remove duplicates based on message content
    initial_count = len(consolidated_df)
    consolidated_df = consolidated_df.drop_duplicates(subset=['message'], keep='first')
    dedupe_count = initial_count - len(consolidated_df)
    
    print("\n" + "=" * 60)
    print("CONSOLIDATION SUMMARY")
    print("=" * 60)
    print(f"Total samples collected: {initial_count}")
    print(f"Duplicates removed: {dedupe_count}")
    print(f"Final dataset size: {len(consolidated_df)}")
    
    # Show sentiment distribution
    print("\nSentiment Distribution:")
    sentiment_counts = consolidated_df['sentiment_category'].value_counts()
    for sentiment, count in sentiment_counts.items():
        percentage = (count / len(consolidated_df)) * 100
        print(f"  {sentiment:20s}: {count:5d} ({percentage:5.1f}%)")
    
    return consolidated_df

def main():
    """Main execution function"""
    
    # Define file mappings (you can adjust paths as needed)
    file_mappings = {
        # From vscode-local (external files)
        '/tmp/conversation_text.csv': process_conversation_text,
        '/tmp/emotion_dataset_v5_clean.csv': process_emotion_dataset,
        '/tmp/Test_Data.csv': process_test_data,
        '/tmp/test.tsv': process_tsv_multilabel,
        '/tmp/data.csv': process_data_csv,
        '/tmp/final_dataset (1).csv': process_final_dataset,
        '/tmp/DATA.txt': process_data_txt,
        '/tmp/Emotion_classify_Data.csv': process_emotion_classify,
        '/tmp/text_emotion.csv': process_text_emotion,
        '/tmp/text_emotion (1).csv': process_text_emotion,
        '/tmp/emotion_tweets.csv': process_emotion_tweets,
        '/tmp/test_predictions_full.csv': process_test_predictions,
        '/tmp/eng.csv': process_eng_csv,
    }
    
    # Process and consolidate all datasets
    consolidated_df = consolidate_all_datasets(file_mappings)
    
    if consolidated_df is not None:
        # Save to the training location
        output_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'data',
            'data_trained.csv'
        )
        
        # Ensure data directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Save consolidated dataset
        consolidated_df.to_csv(output_path, index=False)
        print(f"\n✓ Consolidated dataset saved to: {output_path}")
        print("\n" + "=" * 60)
        print("Training data is ready! You can now run:")
        print("  python run_train_and_test.py")
        print("=" * 60)
        
        return output_path
    else:
        print("\n❌ Failed to create consolidated dataset")
        return None

if __name__ == "__main__":
    main()
