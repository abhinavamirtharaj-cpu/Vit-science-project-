"""
import_external_data.py
Helper script to import external CSV files for training
"""

import shutil
import os

# Mapping of external files to import
EXTERNAL_FILES = [
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
]

def import_files():
    """Copy external files to /tmp for processing"""
    
    print("=" * 60)
    print("IMPORTING EXTERNAL TRAINING FILES")
    print("=" * 60)
    
    copied = 0
    missing = []
    
    for filename in EXTERNAL_FILES:
        source = f"/vscode-local/{filename}"
        dest = f"/tmp/{filename}"
        
        # Try to locate the file in common locations
        possible_locations = [
            f"/vscode-local/{filename}",
            f"vscode-local:/{filename}",
            f"/workspaces/{filename}",
            f"/root/{filename}",
        ]
        
        found = False
        for location in possible_locations:
            if os.path.exists(location):
                try:
                    shutil.copy2(location, dest)
                    print(f"✓ Copied: {filename}")
                    copied += 1
                    found = True
                    break
                except Exception as e:
                    print(f"✗ Error copying {filename}: {e}")
        
        if not found:
            missing.append(filename)
    
    print("\n" + "=" * 60)
    print(f"Successfully copied: {copied} files")
    
    if missing:
        print(f"Missing files: {len(missing)}")
        print("\nPlease place these files in /tmp/ manually:")
        for f in missing:
            print(f"  - {f}")
    
    print("=" * 60)
    
    return copied > 0

if __name__ == "__main__":
    import_files()
