#!/usr/bin/env python3
"""Quick test to verify Hello is classified as Neutral"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core_analysis.chat_service import process_user_message

# Test Hello
contact = {'id': 'test_user', 'name': 'Test'}
result = process_user_message('Hello', contact)

print("="*60)
print("HELLO CLASSIFICATION TEST")
print("="*60)
print(f"Input: 'Hello'")
print(f"Category: {result['sentiment']['category']}")
print(f"Color: {result['sentiment']['color']}")
print(f"Emoji: {result['sentiment']['emoji']}")
print(f"Polarity: {result['sentiment']['polarity']:.3f}")
print("="*60)

if result['sentiment']['category'] == 'Neutral':
    print("✅ SUCCESS: Hello is correctly classified as Neutral!")
    print(f"   Color should be yellow: {result['sentiment']['color']}")
else:
    print(f"❌ FAILED: Hello classified as {result['sentiment']['category']}")
    print(f"   Expected: Neutral, Got: {result['sentiment']['category']}")

print("="*60)
