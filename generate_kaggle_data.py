import csv
import random

# A large synthetic dataset simulating a Kaggle conversation dataset
# Contains varied sentiments and contexts:
# - Customer Support interactions
# - Casual chat
# - Emotional venting
# - Feedback

CATEGORIES = ['Neutral', 'Positive', 'Very Positive', 'Negative', 'Very Negative', 'Sarcastic']

SENTENCES = {
    'Neutral': [
        "I need to check my account balance.", "What time does the store open?", "The package arrived today.",
        "I am reading the documentation.", "Please wait a moment.", "I will check that for you.",
        "The weather is cloudy.", "I have a question about the product.", "Is this compatible with Windows?",
        "My order number is 12345.", "Can you send me the link?", "I am just browsing.",
        "Okay, I understand.", "Let me try that.", "It is working now."
    ],
    'Positive': [
        "Thanks for your help.", "I appreciate the quick response.", "That sounds good.",
        "I like this feature.", "It was easy to set up.", "The delivery was fast.",
        "Good job on the update.", "I am happy with the service.", "This is helpful.",
        "Nice interface.", "Works as expected.", "Cool, thanks.", "I'm glad to hear that.",
        "Have a nice day.", "You too."
    ],
    'Very Positive': [
        "This is amazing!", "I absolutely love it!", "Best customer service ever!",
        "You are a lifesaver!", "Fantastic work!", "I am so excited about this!",
        "Highly recommended!", "Simply the best!", "Wow, that was fast!",
        "I am blown away by the quality.", "Perfect solution!", "Thank you so much!!!",
        "Just what I needed!", "Incredible experience!", "Superb!"
    ],
    'Negative': [
        "It is not working.", "I am having trouble logging in.", "The delivery is late.",
        "I am disappointed.", "This is confusing.", "Why is it so slow?",
        "I don't like the new design.", "The app keeps crashing.", "My payment failed.",
        "I can't find the option.", "This is not what I ordered.", "Please cancel my subscription.",
        "I waited for an hour.", "Nobody replied to my email.", "It is broken."
    ],
    'Very Negative': [
        "This is terrible!", "I am extremely angry!", "Worst experience ever!",
        "I want a refund immediately!", "You ruined my day!", "Unacceptable service!",
        "I will never use this again!", "Complete waste of money!", "Are you kidding me?!",
        "This is a scam!", "Horrible, just horrible!", "I am furious!",
        "Fix this NOW!", "I am deleting my account!", "Total disaster!"
    ],
    'Sarcastic': [
        "Oh great, another error. Just what I needed.", "Yeah, because that makes total sense.",
        "Thanks for nothing.", "Wow, you are so helpful... not.", "Brilliant design, truly.",
        "Oh sure, take your time, I have all day.", "Fantastic, now it's even worse.",
        "I love waiting in line for hours.", "Best update ever... if you like bugs.",
        "Clearly you know what you are doing.", "Oh wow, a generic response. How original.",
        "Thanks for breaking my workflow.", "Genius move.", "Yeah, right.",
        "As if that would work."
    ]
}

def generate_dataset(filename, num_rows=1000):
    from get_resource_path import get_resource_path
    out_path = get_resource_path(filename)
    with open(out_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        # Header matching the project's expectation + extra metadata if needed
        writer.writerow(['contact_id', 'contact_name', 'dir', 'text', 'sentiment_category'])
        
        users = [f"user_{i}" for i in range(1, 51)] # 50 unique users
        
        for _ in range(num_rows):
            user = random.choice(users)
            category = random.choice(CATEGORIES)
            text = random.choice(SENTENCES[category])
            
            # Add some noise/variation to text? No, keep it clean for training patterns.
            # But let's create some "patterns" for specific users to train Node 2 better.
            
            # User 1-10: Tend to be Negative/Sarcastic
            if int(user.split('_')[1]) <= 10:
                if random.random() < 0.7:
                    category = random.choice(['Negative', 'Very Negative', 'Sarcastic'])
                    text = random.choice(SENTENCES[category])
            
            # User 40-50: Tend to be Positive
            elif int(user.split('_')[1]) >= 40:
                if random.random() < 0.7:
                    category = random.choice(['Positive', 'Very Positive'])
                    text = random.choice(SENTENCES[category])
            
            writer.writerow([user, f"User {user.split('_')[1]}", 'sent', text, category])

if __name__ == "__main__":
    generate_dataset('data/data_trained.csv', num_rows=3000)
    print("Generated 3000 rows of synthetic conversation data in data/data_trained.csv")
