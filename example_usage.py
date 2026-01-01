"""
example_usage.py
Example usage of the sentiment analysis system

This script demonstrates how to use the sentiment analyzer and chat service
both programmatically and through the API.
"""

# ============================================================================
# EXAMPLE 1: Direct Sentiment Analysis (Without Flask)
# ============================================================================

from sentiment_analyzer import (
    analyze_emotion,
    analyze_chat_message,
    analyze_historical_context,
    batch_analyze_messages,
    get_sentiment_category
)

print("=" * 70)
print("EXAMPLE 1: Direct Sentiment Analysis")
print("=" * 70)

# Single emotion analysis
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


# ============================================================================
# EXAMPLE 2: Batch Analysis
# ============================================================================

print("\n" + "=" * 70)
print("EXAMPLE 2: Batch Analysis")
print("=" * 70)

messages = [
    "I love this messaging app!",
    "Terrible service, full of bugs.",
    "It's okay, works fine.",
    "This is absolutely amazing!",
    "I hate this, worst experience ever."
]

print("\nAnalyzing multiple messages:\n")
analyses = batch_analyze_messages(messages)

for i, analysis in enumerate(analyses, 1):
    print(f"[{i}] {analysis['input_text']}")
    print(f"    → {analysis['emoji']} {analysis['category']}")
    print(f"    → Polarity: {analysis['polarity_score']:.3f}")
    print()


# ============================================================================
# EXAMPLE 3: Historical Context Analysis
# ============================================================================

print("=" * 70)
print("EXAMPLE 3: Historical Context Analysis")
print("=" * 70)

current_msg = "I'm feeling better now!"
previous_msgs = [
    "This is terrible.",
    "Still frustrated.",
    "Things are improving.",
]

context_analysis = analyze_historical_context(current_msg, previous_msgs)
print(f"\nCurrent Message: '{current_msg}'")
print(f"Previous Messages: {len(context_analysis['context_count'])} messages considered")
print(f"Sentiment Trend: {context_analysis['sentiment_trend']}")
print(f"Category: {context_analysis['category']}")
print(f"Polarity: {context_analysis['polarity_score']:.3f}")


# ============================================================================
# EXAMPLE 4: Using with Chat Service (Local Storage)
# ============================================================================

print("\n" + "=" * 70)
print("EXAMPLE 4: Using Chat Service")
print("=" * 70)

from chat_service import process_user_message

contact = {
    'id': 'example_user',
    'name': 'Example User'
}

message_text = "This is a wonderful experience!"

result = process_user_message(message_text, contact)

print(f"\nMessage: '{message_text}'")
print(f"Sentiment: {result['sentiment']['category']} {result['sentiment']['emoji']}")
print(f"Description: {result['sentiment']['description']}")
print(f"Stored in CSV: {result['stored']}")
print(f"Sentiment Trend: {result['trend']}")


# ============================================================================
# EXAMPLE 5: Using with Storage (Direct CSV Access)
# ============================================================================

print("\n" + "=" * 70)
print("EXAMPLE 5: Storage - Reading Chat History")
print("=" * 70)

from storage import get_history, get_csv_path

print(f"\nCSV File Path: {get_csv_path()}")

history = get_history('example_user')
print(f"\nMessages for 'example_user': {len(history)}")

if history:
    print("\nRecent messages:")
    for msg in history[-3:]:  # Last 3 messages
        print(f"  • {msg['text']}")
        if msg.get('sentiment_category'):
            print(f"    Sentiment: {msg['sentiment_emoji']} {msg['sentiment_category']}")


# ============================================================================
# EXAMPLE 6: API Usage (with Flask Running)
# ============================================================================

print("\n" + "=" * 70)
print("EXAMPLE 6: API Usage (Requires Flask Server Running)")
print("=" * 70)

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
# EXAMPLE 7: Sentiment Color Reference
# ============================================================================

print("\n" + "=" * 70)
print("EXAMPLE 7: Sentiment Color Reference")
print("=" * 70)

print("""
Sentiment colors used in the UI:

🟢 GREEN (#4CAF50)   - Positive sentiments (polarity > 0.1)
   Examples: "I love this!", "That's great!", "Awesome!"

🔴 RED (#F44336)     - Negative sentiments (polarity < -0.1)
   Examples: "This is awful.", "I hate it.", "Terrible."

🟡 YELLOW (#FFC107)  - Neutral sentiments (-0.1 <= polarity <= 0.1)
   Examples: "It's okay.", "Maybe.", "I think so."

Sentiment Categories:
  😄 Very Positive   (polarity > 0.3)
  🙂 Positive        (polarity 0.1 to 0.3)
  😐 Neutral         (polarity -0.1 to 0.1)
  ☹️  Negative       (polarity -0.3 to -0.1)
  😠 Very Negative   (polarity < -0.3)
""")


# ============================================================================
# EXAMPLE 8: Customizing Sentiment Analysis
# ============================================================================

print("\n" + "=" * 70)
print("EXAMPLE 8: Customizing Sentiment Analysis")
print("=" * 70)

print("""
You can customize the sentiment analyzer by editing sentiment_analyzer.py:

1. Change polarity thresholds in get_sentiment_category():
   - Adjust the comparison values (e.g., > 0.3, < -0.3)
   
2. Modify color codes in get_sentiment_color():
   - Change hex color values (#4CAF50, #F44336, #FFC107)
   
3. Add new sentiment categories:
   - Add more emoji and descriptions in get_sentiment_category()
   
4. Extend with custom NLP:
   - Import additional NLP libraries
   - Add sarcasm detection, emotion intensity, etc.

Example modification:
   - Lower thresholds for more sensitive detection
   - Add custom dictionary for domain-specific terms
   - Implement multi-language support with TextBlob
""")


print("\n" + "=" * 70)
print("Examples Complete!")
print("=" * 70)
print("\nFor more information, see:")
print("  - SENTIMENT_ANALYSIS_GUIDE.md")
print("  - QUICK_START.md")
print("  - sentiment_analyzer.py (source code)")
print("\n")
