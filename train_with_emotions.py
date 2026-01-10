"""
train_with_emotions.py
Training pipeline that preserves specific emotion labels instead of consolidating them.
"""

import pandas as pd
import os
from emotion_colors import EMOTION_COLORS

# Keep specific emotions without consolidating
def process_emotion_dataset(filepath, format_type='auto'):
    """Process emotion datasets and keep specific emotion labels"""
    
    print(f"Processing {filepath} with format: {format_type}")
    
    try:
        # Try reading with different encodings
        for encoding in ['utf-8', 'latin-1', 'iso-8859-1']:
            try:
                df = pd.read_csv(filepath, encoding=encoding)
                break
            except:
                continue
        
        processed = []
        
        # Handle different column names
        emotion_col = None
        text_col = None
        
        for col in df.columns:
            col_lower = col.lower()
            if 'emotion' in col_lower or 'sentiment' in col_lower or 'feeling' in col_lower:
                emotion_col = col
            if 'text' in col_lower or 'message' in col_lower or 'content' in col_lower:
                text_col = col
        
        if not emotion_col or not text_col:
            print(f"Warning: Could not find emotion or text columns in {filepath}")
            print(f"Columns: {df.columns.tolist()}")
            return processed
        
        for idx, row in df.iterrows():
            emotion = str(row[emotion_col]).lower().strip()
            text = str(row[text_col]).strip()
            
            if pd.isna(emotion) or pd.isna(text) or text == '' or text == 'nan':
                continue
            
            # Keep the specific emotion (no consolidation)
            if emotion in EMOTION_COLORS:
                processed.append({
                    'contact_id': f'user_{idx}',
                    'message': text,
                    'dir': 'sent',
                    'emotion': emotion  # Keep specific emotion
                })
        
        print(f"Processed {len(processed)} messages from {filepath}")
        return processed
        
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return []

def train_with_detailed_emotions(csv_files=None):
    """Train model with detailed emotion labels"""
    
    if csv_files is None:
        # Find all CSV files in data directory
        csv_files = []
        data_dir = 'data'
        if os.path.exists(data_dir):
            for file in os.listdir(data_dir):
                if file.endswith('.csv') and file not in ['data_trained.csv', 'chat_history_global.csv']:
                    csv_files.append(os.path.join(data_dir, file))
    
    print(f"Found {len(csv_files)} CSV files to process")
    
    all_data = []
    
    # Process each file
    for csv_file in csv_files:
        print(f"\n{'='*60}")
        print(f"Processing: {csv_file}")
        data = process_emotion_dataset(csv_file)
        all_data.extend(data)
    
    if not all_data:
        print("\n❌ No training data found!")
        return
    
    # Create DataFrame
    df = pd.DataFrame(all_data)
    
    # Remove duplicates
    df = df.drop_duplicates(subset=['message'])
    
    print(f"\n{'='*60}")
    print(f"✅ Total unique messages: {len(df)}")
    print(f"\nEmotion distribution:")
    emotion_counts = df['emotion'].value_counts()
    for emotion, count in emotion_counts.items():
        percentage = (count / len(df)) * 100
        print(f"  {emotion}: {count} ({percentage:.1f}%)")
    
    # Save training data
    output_file = 'data/data_trained_emotions.csv'
    df.to_csv(output_file, index=False)
    print(f"\n✅ Saved training data to: {output_file}")
    print(f"Total emotions: {df['emotion'].nunique()}")
    print(f"Emotions: {sorted(df['emotion'].unique())}")
    
    return df

if __name__ == '__main__':
    print("="*60)
    print("EMOTION-BASED TRAINING SYSTEM")
    print("="*60)
    
    # Train with all emotions
    df = train_with_detailed_emotions()
    
    if df is not None:
        print("\n" + "="*60)
        print("✅ TRAINING COMPLETE!")
        print("="*60)
        print(f"\nYou can now use the trained model with {df['emotion'].nunique()} different emotions!")
