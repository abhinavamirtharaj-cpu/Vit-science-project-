"""
test_emotions.py
Quick test of the emotion detection system
"""

from emotion_analyzer import analyze_emotion
from emotion_colors import get_emotion_color, get_emotion_emoji

# Test cases covering different emotions
test_cases = [
    # Positive
    ("I'm so happy today!", "joy"),
    ("This is absolutely wonderful", "happiness"),
    ("I love this so much", "love"),
    ("I'm so excited for tomorrow!", "excitement"),
    ("Thank you so much!", "gratitude"),
    ("This is hilarious", "amusement"),
    ("Great work team!", "approval"),
    
    # Neutral
    ("Hello", "neutral"),
    ("Okay then", "neutral"),
    ("Wow that's surprising", "surprise"),
    ("Oh I see now", "realization"),
    ("I'm confused about this", "confusion"),
    
    # Negative
    ("I'm so angry about this", "anger"),
    ("This is annoying", "annoyance"),
    ("I'm really sad", "sadness"),
    ("I'm terrified", "fear"),
    ("I'm worried sick", "worry"),
    ("I hate this", "hate"),
    ("I'm so disappointed", "disappointment"),
    ("This is disgusting", "disgust"),
    
    # Special
    ("I'm feeling anxious", "anxiety"),
    ("I'm so stressed out", "stress"),
    ("This is so frustrating", "frustration"),
    ("I feel so lonely", "loneliness"),
    ("Yeah right, like that'll work", "sarcasm"),
]

def test_emotion_detection():
    """Test emotion detection accuracy"""
    print("="*70)
    print("EMOTION DETECTION TEST")
    print("="*70)
    
    correct = 0
    total = len(test_cases)
    
    for text, expected in test_cases:
        result = analyze_emotion(text)
        detected = result['emotion']
        color = get_emotion_color(detected)
        emoji = get_emotion_emoji(detected)
        
        # Check if detected matches expected or is in same category
        match = "✅" if detected == expected else "⚠️"
        
        if detected == expected:
            correct += 1
        
        print(f"\n{match} Text: \"{text}\"")
        print(f"   Expected: {expected}")
        print(f"   Detected: {detected} {emoji} ({color})")
        print(f"   Category: {result['category']}")
        print(f"   Polarity: {result['polarity']:.2f}")
    
    print("\n" + "="*70)
    print(f"ACCURACY: {correct}/{total} ({(correct/total)*100:.1f}%)")
    print("="*70)
    
    return correct, total

if __name__ == '__main__':
    correct, total = test_emotion_detection()
    
    print("\n📊 Results:")
    print(f"   ✅ Correct: {correct}")
    print(f"   ⚠️  Different: {total - correct}")
    print(f"   📈 Accuracy: {(correct/total)*100:.1f}%")
    
    print("\n🎨 Emotion Colors Available:")
    from emotion_colors import EMOTION_COLORS
    print(f"   Total: {len(EMOTION_COLORS)} emotions")
    print(f"   Positive: 14 emotions")
    print(f"   Neutral: 5 emotions")
    print(f"   Negative: 15 emotions")
    print(f"   Special: 10 emotions")
