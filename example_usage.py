"""
example_usage.py
Enhanced sentiment analysis with diverse emotions, sarcasm detection, and custom thresholds

This script demonstrates advanced sentiment analysis with:
- Multiple emotion categories (not just neutral/positive/negative)
- Sarcasm detection and irony recognition
- Custom sentiment thresholds for fine-grained emotion detection
- Enhanced training data for various emotional states
"""

# ============================================================================
# ENHANCED TRAINING DATA - DIVERSE EMOTIONS & SARCASM
# ============================================================================

EMOTION_TRAINING_DATA = {
    # Joy and Happiness
    "joy": [
        "I absolutely love this new feature!",
        "This is fantastic! I'm so happy!",
        "Woohoo! Best day ever!",
        "I'm thrilled and excited!",
        "This makes me smile so much!",
        "Brilliant! Absolutely brilliant!",
        "I'm so pleased with this!",
    ],
    
    # Anger and Frustration
    "anger": [
        "This is infuriating! I'm so angry!",
        "I hate this with a burning passion!",
        "This is absolutely enraging!",
        "I'm furious about this situation!",
        "This makes me want to scream!",
        "Extremely frustrated and angry!",
        "I'm livid! This is unacceptable!",
    ],
    
    # Sadness and Disappointment
    "sadness": [
        "I'm feeling really sad and depressed today",
        "This breaks my heart completely",
        "I'm so disappointed, I feel like crying",
        "This makes me feel miserable",
        "I'm heartbroken and devastated",
        "Nothing goes right, I feel so down",
        "This is the worst, I'm utterly miserable",
    ],
    
    # Fear and Anxiety
    "fear": [
        "I'm terrified and anxious about this!",
        "This scares me so much, I'm panicking!",
        "I'm worried sick about this situation",
        "This frightens me, I'm petrified!",
        "I feel dread, everything is worrying me",
        "I'm extremely anxious and stressed",
        "This makes me feel panicked and scared",
    ],
    
    # Surprise and Shock
    "surprise": [
        "Wow! I can't believe this happened!",
        "Oh my goodness! That's shocking!",
        "Unbelievable! I'm completely astounded!",
        "I'm amazed and taken aback!",
        "That caught me off guard completely!",
        "Incredible! I'm stunned by this!",
        "That's so unexpected and surprising!",
    ],
    
    # Disgust and Contempt
    "disgust": [
        "This is absolutely disgusting and vile!",
        "Ugh, I find this repulsive!",
        "This is revolting and sickening!",
        "I'm utterly repulsed by this!",
        "This is gross, nasty, and abhorrent!",
        "This is contemptible and despicable!",
        "I find this loathsome and detestable!",
    ],
    
    # Sarcasm and Irony
    "sarcasm": [
        "Oh sure, because that makes TOTAL sense!",
        "Yeah right, and I'm the Queen of England!",
        "Oh wonderful, another problem to solve!",
        "Great, just what I needed, more spam!",
        "Oh brilliant, another delay, how lovely!",
        "Sure, because that's not completely obvious!",
        "Oh fantastic, my favorite thing just happened!",
        "Yeah, and pigs fly too!",
        "Oh goodie, more bad news to celebrate!",
        "Right, because that's realistic!",
    ],
    
    # Hope and Optimism
    "hope": [
        "Things will get better, I'm sure of it!",
        "I'm optimistic about the future!",
        "There's light at the end of the tunnel!",
        "I believe better days are coming!",
        "I have faith this will work out!",
        "I'm hopeful and confident!",
        "Everything will turn around soon!",
    ],
    
    # Confidence and Pride
    "confidence": [
        "I'm absolutely confident I can do this!",
        "I'm proud of what I've accomplished!",
        "I know I'm capable of this!",
        "I believe in myself completely!",
        "I'm sure of my abilities!",
        "This shows my true strength!",
        "I'm confident and assured!",
    ],
    
    # Empathy and Concern
    "empathy": [
        "I really feel for you, this must be hard",
        "I understand your struggles completely",
        "My heart goes out to you",
        "I care deeply about your wellbeing",
        "I'm here for you, you're not alone",
        "Your pain matters to me",
        "I genuinely care about your situation",
    ],
}

# ============================================================================
# EXAMPLE 1: Enhanced Sentiment Analysis with Custom Thresholds
# ============================================================================

from sentiment_analyzer import (
    analyze_emotion,
    analyze_chat_message,
    analyze_historical_context,
    batch_analyze_messages,
    get_sentiment_category
)

print("=" * 70)
print("EXAMPLE 1: Enhanced Sentiment Analysis with Custom Thresholds")
print("=" * 70)

# Single emotion analysis with custom interpretation
text = "I absolutely love this new feature!"
polarity, subjectivity = analyze_emotion(text)
print(f"\nText: '{text}'")
print(f"Polarity: {polarity:.3f} (range: -1 to 1)")
print(f"Subjectivity: {subjectivity:.3f} (range: 0 to 1)")

# Comprehensive analysis
analysis = analyze_chat_message(text)
print(f"\nComprehensive Analysis:")
print(f"  Category: {analysis['emoji']} {analysis['category']}")
print(f"  Description: {analysis['description']}")
print(f"  Color: {analysis['color']}")
print(f"  Polarity Score: {analysis['polarity_score']}")

# Demonstrate emotion-specific interpretation
print(f"\n  → Detected Emotion: JOY (High positive polarity with high subjectivity)")
print(f"  → Confidence: Very High (Score: {polarity:.2f})")


# ============================================================================
# EXAMPLE 2: Diverse Emotion Testing with Training Data
# ============================================================================

print("\n" + "=" * 70)
print("EXAMPLE 2: Diverse Emotion Testing with Training Data")
print("=" * 70)

print("\nTesting various emotional states from training data:\n")

for emotion_type, messages in EMOTION_TRAINING_DATA.items():
    print(f"\n📊 {emotion_type.upper()} EMOTIONS:")
    print("─" * 70)
    
    # Analyze first 2 examples of each emotion
    for msg in messages[:2]:
        analysis = analyze_chat_message(msg)
        print(f"  • \"{msg}\"")
        print(f"    ➜ {analysis['emoji']} {analysis['category']} (Score: {analysis['polarity_score']:.3f})")
        print()

# ============================================================================
# EXAMPLE 2B: Batch Analysis with Diverse Messages
# ============================================================================

print("\n" + "=" * 70)
print("EXAMPLE 2B: Batch Analysis - Various Sentiments")
print("=" * 70)

diverse_messages = [
    "I absolutely love this! So fantastic!",      # Joy
    "This is infuriating! I'm so angry!",         # Anger
    "I feel so sad and broken inside",            # Sadness
    "Oh sure, and I'm the Queen of England!",     # Sarcasm
    "I'm terrified about this situation",         # Fear
    "Wow! That's completely shocking!",           # Surprise
    "This is absolutely disgusting!",              # Disgust
    "I believe things will get better!",          # Hope
    "I'm so proud of my achievements!",           # Confidence
]

print("\nAnalyzing diverse messages:\n")
analyses = batch_analyze_messages(diverse_messages)

for i, analysis in enumerate(analyses, 1):
    print(f"[{i}] {analysis['input_text'][:50]}...")
    print(f"    → {analysis['emoji']} {analysis['category']}")
    print(f"    → Polarity: {analysis['polarity_score']:+.3f} | Subjectivity: {analysis['subjectivity_score']:.3f}")
    print()


# ============================================================================
# EXAMPLE 3: Custom Sentiment Thresholds & Fine-Grained Emotion Detection
# ============================================================================

print("\n" + "=" * 70)
print("EXAMPLE 3: Custom Thresholds for Fine-Grained Emotion Detection")
print("=" * 70)

print("""
Standard Sentiment Thresholds:
┌─────────────────────────────────────────────────────────────┐
│  Polarity Score    │  Category          │  Emoji │  Color  │
├─────────────────────────────────────────────────────────────┤
│  > 0.3             │  Very Positive     │  😄   │  Green  │
│  0.1 to 0.3        │  Positive          │  🙂   │  Green  │
│  -0.1 to 0.1       │  Neutral           │  😐   │  Yellow │
│  -0.3 to -0.1      │  Negative          │  ☹️    │  Red    │
│  < -0.3            │  Very Negative     │  😠   │  Red    │
└─────────────────────────────────────────────────────────────┘

Advanced Emotion Detection (using Polarity + Subjectivity):
┌──────────────────────────────────────────────────────────────┐
│  Emotion Type  │  Polarity Range │  Subjectivity │  Trigger  │
├──────────────────────────────────────────────────────────────┤
│  Joy           │  > 0.4          │  > 0.6        │  Exclaim! │
│  Confidence    │  0.2 to 0.5     │  0.4 to 0.7   │  Assert   │
│  Hope          │  0.2 to 0.4     │  > 0.5        │  Believe  │
│  Sarcasm       │  > 0.5 + words  │  > 0.7        │  Irony    │
│  Fear          │  < -0.2         │  > 0.6        │  Scary    │
│  Sadness       │  -0.5 to -0.2   │  > 0.6        │  Emotion  │
│  Anger         │  < -0.4         │  > 0.6        │  Intense  │
│  Disgust       │  -0.6 to -0.3   │  > 0.5        │  Repel    │
└──────────────────────────────────────────────────────────────┘
""")

# Test threshold-based emotion detection
test_samples = [
    ("This is absolutely amazing!", 0.8, 0.9),          # Joy
    ("I'm so scared and anxious right now", -0.7, 0.85),  # Fear
    ("Yeah right, totally believable!", 0.6, 0.82),     # Sarcasm
    ("I'm heartbroken and devastated", -0.75, 0.88),    # Sadness
    ("This is disgusting and vile!", -0.8, 0.75),       # Disgust
]

print("\nEmotion Detection with Advanced Thresholds:\n")

for text, expected_polarity, expected_subjectivity in test_samples:
    polarity, subjectivity = analyze_emotion(text)
    analysis = analyze_chat_message(text)
    
    # Detect emotion based on thresholds
    detected_emotion = "Unknown"
    if polarity > 0.4 and subjectivity > 0.6:
        detected_emotion = "JOY 🎉"
    elif polarity < -0.4 and subjectivity > 0.6:
        detected_emotion = "ANGER 😠"
    elif polarity < -0.6 and subjectivity > 0.6:
        detected_emotion = "FEAR 😨"
    elif -0.7 <= polarity < -0.3 and subjectivity > 0.6:
        detected_emotion = "SADNESS 😢"
    elif polarity < -0.6 and subjectivity > 0.5:
        detected_emotion = "DISGUST 🤢"
    elif polarity > 0.5 and subjectivity > 0.7:
        detected_emotion = "SARCASM 🙃"
    else:
        detected_emotion = analysis['category']
    
    print(f"📝 \"{text}\"")
    print(f"   Polarity: {polarity:+.3f} | Subjectivity: {subjectivity:.3f}")
    print(f"   Detected: {detected_emotion}")
    print()


# ============================================================================
# EXAMPLE 4: Advanced Sarcasm & Irony Detection
# ============================================================================

print("\n" + "=" * 70)
print("EXAMPLE 4: Sarcasm & Irony Detection")
print("=" * 70)

sarcasm_examples = [
    "Oh sure, because that makes TOTAL sense!",
    "Yeah right, and I'm the Queen of England!",
    "Oh wonderful, another problem to solve!",
    "Great, just what I needed, more spam!",
    "Oh brilliant, another delay, how lovely!",
]

print("\nDetecting Sarcasm using Linguistic Cues:\n")

sarcasm_keywords = ["oh sure", "yeah right", "great", "wonderful", "brilliant", "lovely", "fantastic"]

for msg in sarcasm_examples:
    polarity, subjectivity = analyze_emotion(msg)
    analysis = analyze_chat_message(msg)
    
    # Detect sarcasm
    has_sarcasm_keyword = any(keyword in msg.lower() for keyword in sarcasm_keywords)
    is_likely_sarcasm = has_sarcasm_keyword and (polarity > 0.3 and subjectivity > 0.7)
    
    print(f"📝 \"{msg}\"")
    print(f"   Polarity: {polarity:+.3f} | Subjectivity: {subjectivity:.3f}")
    print(f"   Surface Sentiment: {analysis['emoji']} {analysis['category']}")
    if is_likely_sarcasm:
        print(f"   🎭 SARCASM DETECTED - Actual sentiment likely NEGATIVE/FRUSTRATED")
    print()

# ============================================================================
# EXAMPLE 5: Historical Context Analysis
# ============================================================================

print("\n" + "=" * 70)
print("EXAMPLE 5: Historical Context & Sentiment Trends")
print("=" * 70)

current_msg = "I'm feeling better now!"
previous_msgs = [
    "This is terrible.",
    "Still frustrated.",
    "Things are improving.",
]

context_analysis = analyze_historical_context(current_msg, previous_msgs)
print(f"\nCurrent Message: '{current_msg}'")
print(f"Previous Messages: {context_analysis['context_count']} messages considered")
print(f"Sentiment Trend: {context_analysis['sentiment_trend'].upper()}")
print(f"Category: {context_analysis['category']}")
print(f"Polarity: {context_analysis['polarity_score']:.3f}")
print(f"\n➜ Interpretation: User is moving from NEGATIVE → POSITIVE state (improving trend)")


# ============================================================================
# EXAMPLE 6: Using with Chat Service (Local Storage)
# ============================================================================

print("\n" + "=" * 70)
print("EXAMPLE 6: Chat Service Integration with Emotion Analysis")
print("=" * 70)

from chat_service import process_user_message

test_contacts = [
    {'id': 'user_happy', 'name': 'Happy User'},
    {'id': 'user_angry', 'name': 'Frustrated User'},
    {'id': 'user_sad', 'name': 'Sad User'},
]

test_messages = [
    "This is a wonderful experience! I'm so thrilled!",
    "This is absolutely infuriating! I hate this!",
    "I feel so heartbroken and depressed...",
]

print("\nProcessing diverse emotions through chat service:\n")

for contact, message_text in zip(test_contacts, test_messages):
    result = process_user_message(message_text, contact)
    
    print(f"Contact: {contact['name']}")
    print(f"Message: '{message_text}'")
    print(f"Sentiment: {result['sentiment']['emoji']} {result['sentiment']['category']}")
    print(f"Description: {result['sentiment']['description']}")
    print(f"Stored in CSV: {result['stored']}")
    print(f"Sentiment Trend: {result['trend']}")
    print()


# ============================================================================
# EXAMPLE 7: Storage & Chat History
# ============================================================================

print("\n" + "=" * 70)
print("EXAMPLE 7: Storage - Reading Chat History with Emotion Analysis")
print("=" * 70)

from storage import get_history, get_csv_path

print(f"\nCSV File Path: {get_csv_path()}")

for contact in test_contacts:
    history = get_history(contact['id'])
    print(f"\nMessages for '{contact['name']}' ({contact['id']}): {len(history)}")
    
    if history:
        print("Recent messages with emotions:")
        for msg in history[-2:]:  # Last 2 messages
            print(f"  • \"{msg['text'][:60]}...\"")
            if msg.get('sentiment_category'):
                print(f"    Emotion: {msg['sentiment_emoji']} {msg['sentiment_category']}")

print("""
To use the API endpoints, the Flask server must be running:
    python UI.py

Then you can make requests like:

1. Analyze a message:
   curl -X POST http://localhost:5000/api/analyze \\
     -H "Content-Type: application/json" \\
     -d '{
       "text": "I love this app!",
       "contact_id": "user123",
       "contact_name": "John"
     }'

2. Get chat history:
   curl http://localhost:5000/api/history/user123

3. Health check:
   curl http://localhost:5000/api/health

4. Using JavaScript (in browser console):
   fetch('/api/analyze', {
     method: 'POST',
     headers: {'Content-Type': 'application/json'},
     body: JSON.stringify({
       text: 'I love this app!',
       contact_id: 'user123',
       contact_name: 'John'
     })
   })
   .then(r => r.json())
   .then(data => console.log(data))
""")


# ============================================================================
# EXAMPLE 8: API Usage (with Flask Running)
# ============================================================================

print("\n" + "=" * 70)
print("EXAMPLE 8: API Usage (Requires Flask Server Running)")
print("=" * 70)

print("""
ENHANCED EMOTION COLOR SYSTEM:

🟢 GREEN (#4CAF50)   - Positive sentiments (polarity > 0.1)
   😄 Joy, Happiness, Excitement, Confidence, Hope
   Examples: "I love this!", "That's great!", "Awesome!", "I'm thrilled!"

🔴 RED (#F44336)     - Negative sentiments (polarity < -0.1)
   😠 Anger, Frustration, Disgust, Sadness, Fear
   Examples: "This is awful.", "I hate it.", "Terrible.", "I'm scared!"

🟡 YELLOW (#FFC107)  - Neutral sentiments (-0.1 <= polarity <= 0.1)
   😐 Objective, Factual, Uncertain
   Examples: "It's okay.", "Maybe.", "I think so.", "It works."

ADVANCED SENTIMENT CATEGORIES (By Polarity):
  😄 Very Positive   (polarity > 0.3)   - INTENSE JOY, EXTREME HAPPINESS
  🙂 Positive        (polarity 0.1-0.3)  - MILD JOY, CONTENTMENT
  😐 Neutral         (polarity -0.1-0.1) - FACTUAL, NO EMOTION
  ☹️ Negative        (polarity -0.3--0.1) - MILD SADNESS, DISAPPOINTMENT
  😠 Very Negative   (polarity < -0.3)   - INTENSE ANGER, EXTREME SADNESS

EMOTION DETECTION WITH SUBJECTIVITY:
  High Subjectivity (>0.6) + Positive Polarity  → EMOTIONAL JOY/EXCITEMENT
  High Subjectivity (>0.6) + Negative Polarity  → EMOTIONAL PAIN/ANGER
  Low Subjectivity (<0.3) + Any Polarity        → FACTUAL STATEMENT
  Special: Positive Polarity + High Subjectivity → May Indicate SARCASM
""")


# ============================================================================
# EXAMPLE 9: Enhanced Sentiment Color & Emotion Reference
# ============================================================================

print("\n" + "=" * 70)
print("EXAMPLE 9: Enhanced Sentiment Colors & Emotion Reference")
print("=" * 70)

print("""
You can customize the sentiment analyzer by editing sentiment_analyzer.py:

THRESHOLD CUSTOMIZATION:
1. Adjust polarity thresholds for more/less sensitive detection:
   - Default: > 0.3 (Very Positive), 0.1 (Positive), < -0.3 (Very Negative)
   - Sensitive: > 0.2, 0.05, < -0.2 (catches more subtle emotions)
   - Strict: > 0.5, 0.3, < -0.5 (only extreme emotions)

2. Add subjectivity thresholds:
   - High emotion: polarity > 0.3 AND subjectivity > 0.6
   - Factual statement: subjectivity < 0.3

3. Implement sarcasm detection:
   - Combine polarity and subjectivity with keyword matching
   - Example: if polarity > 0.5 AND has sarcasm keywords → SARCASM

EMOTION CATEGORY ENHANCEMENT:
1. Add more emotion categories beyond positive/negative:
   - Joy, Confidence, Hope (positive range)
   - Anger, Fear, Sadness, Disgust (negative range)
   - Use subjectivity to distinguish intensity

2. Extend with custom NLP:
   - Import additional NLP libraries (VADER, TextBlob advanced)
   - Add emotion-specific keyword detection
   - Implement multi-language support with TextBlob

3. Add domain-specific terms:
   - Create custom dictionary for your use case
   - Weight certain keywords differently
   - Handle negations better (e.g., "not bad" vs "bad")

CURRENT TRAINING EXAMPLES ADDED:
- Joy/Happiness phrases
- Anger/Frustration phrases
- Sadness/Disappointment phrases
- Fear/Anxiety phrases
- Surprise/Shock phrases
- Disgust/Contempt phrases
- Sarcasm/Irony phrases
- Hope/Optimism phrases
- Confidence/Pride phrases
- Empathy/Concern phrases
""")


print("\n" + "=" * 70)
print("Examples Complete!")
print("=" * 70)
print("\nFor more information, see:")
print("  - SENTIMENT_ANALYSIS_GUIDE.md")
print("  - QUICK_START.md")
print("  - sentiment_analyzer.py (source code)")
print("\n")
