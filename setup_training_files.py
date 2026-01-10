#!/usr/bin/env python3
"""
setup_training_files.py
Interactive script to set up training files from external sources
"""

import os
import sys

def show_instructions():
    """Display instructions for setting up training data"""
    
    print("=" * 70)
    print("  TRAINING DATA SETUP - EXTERNAL CSV FILES")
    print("=" * 70)
    
    print("\n📋 INSTRUCTIONS:")
    print("-" * 70)
    print("""
You have provided multiple emotion/sentiment CSV files. To train the model:

OPTION 1: COPY FILES TO WORKSPACE (RECOMMENDED)
-----------------------------------------------
Copy all your CSV files to one of these locations:

  /workspaces/SCIVIT-Draft/training_data/
  or
  /tmp/

Then run:
  python train_with_external_data.py


OPTION 2: SPECIFY FILE PATHS
-----------------------------
Edit the file paths in train_with_external_data.py to point to your files


OPTION 3: USE WGET/CURL
------------------------
If your files are accessible via URL, download them:
  
  cd /tmp
  wget <your-file-url>
  
Then run:
  python train_with_external_data.py


YOUR FILES:
-----------
The training system supports these formats:

1.  conversation_text.csv          - emotion_label, text, conversation_id
2.  emotion_dataset_v5_clean.csv   - sentence, emotion, cleaned_text  
3.  Test_Data.csv                  - Subtitle, Emotion
4.  test.tsv                       - text, Joy, Fear, Anger, Sadness, etc.
5.  data.csv                       - text, labels (numeric 0-7)
6.  final_dataset (1).csv          - text, emotion
7.  DATA.txt                       - text;emotion format
8.  Emotion_classify_Data.csv      - Comment, Emotion
9.  text_emotion.csv               - content, sentiment, author
10. text_emotion (1).csv           - Same format as above
11. emotion_tweets.csv             - Tweet, Emotion
12. test_predictions_full.csv      - originaltweet, sentiment_category
13. eng.csv                        - text, Anger, Fear, Joy, Sadness
    """)
    
    print("=" * 70)
    print("\n🚀 QUICK START:")
    print("-" * 70)
    print("""
# Create training data directory
mkdir -p /workspaces/SCIVIT-Draft/training_data

# Copy your files there (example)
cp /path/to/your/files/*.csv /workspaces/SCIVIT-Draft/training_data/

# Or use the download assistant (if you provide file locations)
    """)
    
    print("=" * 70)
    
    return True

def check_for_files():
    """Check common locations for training files"""
    
    print("\n🔍 CHECKING FOR TRAINING FILES...")
    print("-" * 70)
    
    search_paths = [
        '/workspaces/SCIVIT-Draft/training_data',
        '/tmp',
        '/workspaces/SCIVIT-Draft',
        os.path.expanduser('~'),
    ]
    
    file_patterns = [
        'conversation_text.csv',
        'emotion_dataset_v5_clean.csv',
        'Test_Data.csv',
        'test.tsv',
        'data.csv',
        'final_dataset',
        'DATA.txt',
        'Emotion_classify_Data.csv',
        'text_emotion',
        'emotion_tweets.csv',
        'test_predictions',
        'eng.csv',
    ]
    
    found_files = []
    
    for search_path in search_paths:
        if os.path.exists(search_path) and os.path.isdir(search_path):
            for file in os.listdir(search_path):
                for pattern in file_patterns:
                    if pattern in file and file.endswith(('.csv', '.tsv', '.txt')):
                        full_path = os.path.join(search_path, file)
                        found_files.append(full_path)
                        print(f"  ✓ Found: {full_path}")
    
    if found_files:
        print(f"\n✓ Found {len(found_files)} potential training files!")
        print("\nYou can now run:")
        print("  python train_with_external_data.py")
        return True
    else:
        print("\n⚠ No training files found in common locations")
        return False

def create_training_directory():
    """Create a dedicated training_data directory"""
    
    training_dir = '/workspaces/SCIVIT-Draft/training_data'
    
    try:
        os.makedirs(training_dir, exist_ok=True)
        print(f"\n✓ Created training directory: {training_dir}")
        print(f"\nPlace your CSV files here, then run:")
        print(f"  python train_with_external_data.py")
        return training_dir
    except Exception as e:
        print(f"\n✗ Error creating directory: {e}")
        return None

def main():
    """Main setup function"""
    
    show_instructions()
    
    # Check if files already exist
    if not check_for_files():
        # Create training directory
        create_training_directory()
    
    print("\n" + "=" * 70)
    print("  NEXT STEPS")
    print("=" * 70)
    print("""
1. Copy your CSV files to /workspaces/SCIVIT-Draft/training_data/ or /tmp/
2. Run: python train_with_external_data.py
3. The system will automatically detect and process all files
4. Once training is complete, test with: python run_train_and_test.py
    """)
    print("=" * 70)

if __name__ == "__main__":
    main()
