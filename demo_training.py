"""
demo_training.py
Demonstration of the training system with sample emotion data
"""

import os
import pandas as pd

def create_sample_datasets():
    """Create sample CSV files to demonstrate training"""
    
    training_dir = '/workspaces/SCIVIT-Draft/training_data'
    os.makedirs(training_dir, exist_ok=True)
    
    print("=" * 60)
    print("CREATING SAMPLE TRAINING DATASETS")
    print("=" * 60)
    
    # Sample 1: Simple emotion dataset
    sample1 = pd.DataFrame({
        'text': [
            'I absolutely love this!',
            'This is terrible',
            'Okay, I guess',
            'Not bad at all',
            'This is the worst thing ever',
            'Fantastic work everyone!',
            'Meh, whatever',
            'I hate when this happens',
            'Pretty good stuff',
            'Completely disappointed',
        ],
        'emotion': ['joy', 'anger', 'neutral', 'happiness', 'sadness', 
                   'joy', 'neutral', 'anger', 'happiness', 'sadness']
    })
    
    sample1_path = os.path.join(training_dir, 'sample_emotions.csv')
    sample1.to_csv(sample1_path, index=False)
    print(f"✓ Created: sample_emotions.csv ({len(sample1)} samples)")
    
    # Sample 2: Conversation flow
    sample2 = pd.DataFrame({
        'conversation_id': [1, 1, 1, 2, 2, 2, 3, 3, 3, 3],
        'text': [
            'Hello, how can I help?',
            'My device is not working',
            'Let me fix that for you',
            'Thanks for your help!',
            'Happy to assist',
            'Have a great day!',
            'I am so frustrated',
            'Oh great, another problem',
            'Just perfect',
            'Nothing ever works',
        ],
        'emotion_label': ['neutral', 'neutral', 'neutral', 'joy', 'joy', 'joy',
                         'anger', 'anger', 'sarcasm', 'sadness']
    })
    
    sample2_path = os.path.join(training_dir, 'sample_conversations.csv')
    sample2.to_csv(sample2_path, index=False)
    print(f"✓ Created: sample_conversations.csv ({len(sample2)} samples)")
    
    # Sample 3: Multi-emotion with scores
    sample3 = pd.DataFrame({
        'text': [
            'Best day ever!',
            'So scared right now',
            'Really angry about this',
            'Feeling very sad',
            'What a surprise!',
        ],
        'Joy': [3, 0, 0, 0, 1],
        'Fear': [0, 3, 0, 0, 0],
        'Anger': [0, 0, 3, 0, 0],
        'Sadness': [0, 0, 0, 3, 0],
        'Surprise': [0, 0, 0, 0, 3],
    })
    
    sample3_path = os.path.join(training_dir, 'sample_multilabel.csv')
    sample3.to_csv(sample3_path, index=False)
    print(f"✓ Created: sample_multilabel.csv ({len(sample3)} samples)")
    
    print("\n" + "=" * 60)
    print(f"Sample datasets created in: {training_dir}")
    print("=" * 60)
    
    return [sample1_path, sample2_path, sample3_path]

def run_demo_training():
    """Run a complete demonstration of the training pipeline"""
    
    print("\n" + "=" * 60)
    print("DEMO: TRAINING WITH SAMPLE DATA")
    print("=" * 60)
    
    # Create sample files
    sample_files = create_sample_datasets()
    
    print("\n📚 Training with these sample files:")
    for f in sample_files:
        print(f"  - {os.path.basename(f)}")
    
    print("\n🚀 Now run the training pipeline:")
    print("  python train_with_external_data.py")
    
    print("\n" + "=" * 60)
    print("NOTE: Replace these sample files with your actual data!")
    print("=" * 60)
    
    return sample_files

if __name__ == "__main__":
    run_demo_training()
