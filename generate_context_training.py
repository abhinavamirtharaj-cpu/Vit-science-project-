"""
Context-Aware Training Data Generator
Creates examples of ambiguous phrases in different contexts
"""
import pandas as pd

# Ambiguous phrases with multiple possible emotions based on context
CONTEXT_SCENARIOS = {
    # "Oh my god!" scenarios
    'oh_my_god': {
        'anger': [
            "You broke my laptop! Oh my god!",
            "They canceled the concert! Oh my god!",
            "He lied to me again! Oh my god!",
            "This is the worst day ever! Oh my god!",
            "I can't believe you did that! Oh my god!",
            "Mind your words! Oh my god, the disrespect!",
            "What the hell is wrong with you! Oh my god!",
            "Are you kidding me right now? Oh my god!",
            "This is so frustrating! Oh my god!",
            "I'm so done with this! Oh my god!",
        ],
        'surprise': [
            "I won the lottery! Oh my god!",
            "You're getting married! Oh my god!",
            "Is that really you? Oh my god!",
            "This is unexpected! Oh my god!",
            "I can't believe this! Oh my god!",
            "Did you see that? Oh my god!",
            "Look at that view! Oh my god!",
            "This is incredible! Oh my god!",
            "You did this for me? Oh my god!",
            "I never expected this! Oh my god!",
        ],
        'excitement': [
            "We're going to Paris! Oh my god!",
            "I got accepted! Oh my god!",
            "This is happening! Oh my god!",
            "I'm so excited! Oh my god!",
            "Best news ever! Oh my god!",
            "Can't wait! Oh my god!",
            "This is amazing! Oh my god!",
            "I'm pumped! Oh my god!",
            "Let's do this! Oh my god!",
            "Dreams coming true! Oh my god!",
        ],
        'fear': [
            "There's someone in the house! Oh my god!",
            "The car is coming straight at us! Oh my god!",
            "We're going to crash! Oh my god!",
            "That's terrifying! Oh my god!",
            "I'm so scared! Oh my god!",
            "What was that noise? Oh my god!",
            "It's a spider! Oh my god!",
            "I think someone is following us! Oh my god!",
            "The building is on fire! Oh my god!",
            "We're trapped! Oh my god!",
        ],
        'sadness': [
            "He passed away... Oh my god...",
            "I failed the exam. Oh my god.",
            "They broke up with me. Oh my god...",
            "I lost everything. Oh my god.",
            "This is heartbreaking. Oh my god...",
            "I can't believe they're gone. Oh my god.",
            "My dog died. Oh my god...",
            "Everything is falling apart. Oh my god.",
            "I'm so devastated. Oh my god...",
            "This hurts so much. Oh my god.",
        ],
    },
    
    # "Wow" scenarios
    'wow': {
        'excitement': [
            "We won the championship! Wow!",
            "This is incredible! Wow!",
            "Best present ever! Wow!",
            "I can't believe this is real! Wow!",
            "This is amazing! Wow!",
            "Wow! This is the best day ever!",
            "Wow! I'm so happy!",
            "Wow! This is fantastic!",
        ],
        'surprise': [
            "Did you see that? Wow!",
            "I wasn't expecting this. Wow.",
            "That's unexpected. Wow.",
            "Wow, I'm speechless.",
            "Wow, never saw that coming.",
            "That's a surprise. Wow.",
        ],
        'anger': [
            "You did what? Wow.",
            "Wow, just wow. I'm furious.",
            "Wow, that's disrespectful.",
            "I can't believe you lied. Wow.",
            "Wow, this is unacceptable.",
            "You crossed the line. Wow.",
        ],
        'sarcasm': [
            "Wow, real smart move there.",
            "Wow, brilliant idea. Not.",
            "Oh wow, didn't see that coming. Sarcasm.",
            "Wow, you're a genius. Sure.",
            "Wow, that's just great. Perfect.",
        ],
        'disappointment': [
            "You forgot my birthday. Wow.",
            "Wow, I expected more from you.",
            "That's all you did? Wow.",
            "Wow, I'm let down.",
            "Wow, this is disappointing.",
        ],
    },
    
    # "Great" scenarios
    'great': {
        'happiness': [
            "That's great news!",
            "Great job on the project!",
            "Great to hear from you!",
            "Having a great time!",
            "Feeling great today!",
        ],
        'sarcasm': [
            "Great, just great. My car broke down.",
            "Oh great, another problem.",
            "Great, now everything is ruined.",
            "That's just great. Sarcasm.",
            "Great, perfect timing. Not.",
        ],
        'anger': [
            "Great, you ruined everything!",
            "Great job breaking my trust!",
            "Just great! Now I'm furious!",
            "Oh great, you did it again!",
        ],
    },
    
    # "Perfect" scenarios
    'perfect': {
        'happiness': [
            "Perfect day!",
            "This is perfect!",
            "Perfect timing!",
            "Everything is perfect!",
        ],
        'sarcasm': [
            "Perfect, just perfect. My day is ruined.",
            "Oh perfect, another mistake.",
            "Perfect, now nothing works.",
            "That's perfect. Sarcasm.",
        ],
        'anger': [
            "Perfect! You broke it!",
            "Oh perfect, you lost it!",
            "Just perfect! I'm so angry!",
        ],
    },
    
    # "Nice" scenarios
    'nice': {
        'happiness': [
            "That's nice of you!",
            "Nice work!",
            "Nice to meet you!",
            "Having a nice day!",
        ],
        'sarcasm': [
            "Oh nice, real nice. Sarcasm.",
            "Nice going, you broke it.",
            "Nice job ruining everything.",
            "Real nice. Not.",
        ],
    },
    
    # "Seriously" scenarios
    'seriously': {
        'anger': [
            "Seriously? You did this again!",
            "Are you seriously doing this?",
            "Seriously, I'm fed up!",
            "You can't be serious! I'm furious!",
        ],
        'surprise': [
            "Seriously? That's amazing!",
            "Seriously? I can't believe it!",
            "Are you serious? Wow!",
        ],
        'disappointment': [
            "Seriously? That's all?",
            "Seriously, I expected more.",
            "Are you seriously giving up?",
        ],
    },
    
    # Anger contextual phrases
    'anger_phrases': {
        'anger': [
            "Mind your words!",
            "Watch your mouth!",
            "What the hell are you doing!",
            "What the fish is this!",
            "Shut up right now!",
            "Get lost!",
            "Leave me alone!",
            "You're crossing the line!",
            "Don't test me!",
            "I'm warning you!",
            "Back off!",
            "Cut it out!",
            "Stop it!",
            "Enough is enough!",
            "That's it! I'm done!",
            "You're pissing me off!",
            "Don't push me!",
            "I've had it!",
            "You're getting on my nerves!",
            "Knock it off!",
        ],
    },
}

def generate_context_training():
    """Generate contextual training data"""
    all_data = []
    user_id = 0
    
    print("Generating context-aware training data...")
    print("="*70)
    
    for scenario_name, emotions in CONTEXT_SCENARIOS.items():
        print(f"\nScenario: {scenario_name}")
        for emotion, examples in emotions.items():
            print(f"  {emotion}: {len(examples)} examples")
            for text in examples:
                all_data.append({
                    'contact_id': f'context_{user_id}',
                    'message': text,
                    'dir': 'sent',
                    'emotion': emotion
                })
                user_id += 1
    
    df = pd.DataFrame(all_data)
    output_file = 'data/context_aware_training.csv'
    df.to_csv(output_file, index=False)
    
    print(f"\n{'='*70}")
    print(f"✅ Context training data saved: {output_file}")
    print(f"Total examples: {len(df):,}")
    print(f"\nEmotion distribution:")
    print(df['emotion'].value_counts())
    
    return df

if __name__ == '__main__':
    generate_context_training()
