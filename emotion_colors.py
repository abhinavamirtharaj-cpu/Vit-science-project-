"""
emotion_colors.py
Comprehensive emotion color palette with unique colors for each emotion.
"""

# Complete Emotion to Color Mapping (30+ emotions)
EMOTION_COLORS = {
    # Positive emotions (Greens, Blues, Purples)
    'joy': '#00E676',              # Bright green
    'happiness': '#76FF03',        # Lime green  
    'love': '#FF4081',             # Pink (love color)
    'excitement': '#FFD600',       # Bright yellow
    'enthusiasm': '#FFC400',       # Amber
    'fun': '#FF6E40',              # Deep orange (playful)
    'admiration': '#7C4DFF',       # Deep purple
    'amusement': '#FFAB40',        # Orange
    'approval': '#69F0AE',         # Light green
    'caring': '#F06292',           # Light pink
    'gratitude': '#4FC3F7',        # Light blue
    'relief': '#81C784',           # Medium green
    'pride': '#9575CD',            # Medium purple
    'optimism': '#FFD54F',         # Light yellow
    
    # Neutral emotions (Grays, Yellows, Teals)
    'neutral': '#90A4AE',          # Blue gray
    'surprise': '#FFEB3B',         # Yellow
    'realization': '#26C6DA',      # Cyan
    'confusion': '#B0BEC5',        # Light gray
    'curiosity': '#4DD0E1',        # Light cyan
    
    # Negative emotions (Reds, Dark colors)
    'anger': '#F44336',            # Red
    'annoyance': '#FF7043',        # Deep orange
    'disapproval': '#FF5252',      # Red accent
    'sadness': '#5C6BC0',          # Indigo
    'fear': '#7E57C2',             # Deep purple
    'worry': '#AB47BC',            # Purple
    'hate': '#D32F2F',             # Dark red
    'grief': '#512DA8',            # Deep indigo
    'nervousness': '#BA68C8',      # Light purple
    'disgust': '#8D6E63',          # Brown
    'disappointment': '#E64A19',   # Deep orange
    'embarrassment': '#EC407A',    # Pink
    'shame': '#C62828',            # Dark red
    'guilt': '#AD1457',            # Dark pink
    'remorse': '#6A1B9A',          # Dark purple
    
    # Special emotions
    'sarcasm': '#9C27B0',          # Purple
    'sarcastic': '#9C27B0',        # Purple
    'empathy': '#26A69A',          # Teal
    'anxiety': '#5E35B1',          # Deep purple
    'depression': '#455A64',       # Dark gray
    'stress': '#FF6F00',           # Dark orange
    'frustration': '#EF5350',      # Light red
    'jealousy': '#388E3C',         # Dark green
    'loneliness': '#546E7A',       # Gray blue
    'boredom': '#78909C',          # Medium gray
}

# Emoji mappings for each emotion
EMOTION_EMOJIS = {
    # Positive
    'joy': '😄',
    'happiness': '😊',
    'love': '❤️',
    'excitement': '🤩',
    'enthusiasm': '🎉',
    'fun': '😆',
    'admiration': '😍',
    'amusement': '😂',
    'approval': '👍',
    'caring': '🤗',
    'gratitude': '🙏',
    'relief': '😌',
    'pride': '😤',
    'optimism': '✨',
    
    # Neutral
    'neutral': '😐',
    'surprise': '😲',
    'realization': '💡',
    'confusion': '😕',
    'curiosity': '🤔',
    
    # Negative
    'anger': '😠',
    'annoyance': '😒',
    'disapproval': '👎',
    'sadness': '😢',
    'fear': '😨',
    'worry': '😟',
    'hate': '😡',
    'grief': '😭',
    'nervousness': '😰',
    'disgust': '🤢',
    'disappointment': '😞',
    'embarrassment': '😳',
    'shame': '😔',
    'guilt': '😖',
    'remorse': '😣',
    
    # Special
    'sarcasm': '😏',
    'sarcastic': '😏',
    'empathy': '🫂',
    'anxiety': '😧',
    'depression': '😶',
    'stress': '😫',
    'frustration': '😤',
    'jealousy': '😒',
    'loneliness': '🥺',
    'boredom': '😑',
}

# Emotion categories for grouping
EMOTION_CATEGORIES = {
    'positive': ['joy', 'happiness', 'love', 'excitement', 'enthusiasm', 'fun', 
                 'admiration', 'amusement', 'approval', 'caring', 'gratitude', 
                 'relief', 'pride', 'optimism'],
    'neutral': ['neutral', 'surprise', 'realization', 'confusion', 'curiosity'],
    'negative': ['anger', 'annoyance', 'disapproval', 'sadness', 'fear', 'worry',
                 'hate', 'grief', 'nervousness', 'disgust', 'disappointment',
                 'embarrassment', 'shame', 'guilt', 'remorse'],
    'special': ['sarcasm', 'sarcastic', 'empathy', 'anxiety', 'depression', 
                'stress', 'frustration', 'jealousy', 'loneliness', 'boredom']
}

def get_emotion_color(emotion):
    """Get hex color for an emotion"""
    emotion_lower = emotion.lower()
    return EMOTION_COLORS.get(emotion_lower, '#90A4AE')  # Default to neutral gray

def get_emotion_emoji(emotion):
    """Get emoji for an emotion"""
    emotion_lower = emotion.lower()
    return EMOTION_EMOJIS.get(emotion_lower, '😐')  # Default to neutral face

def get_emotion_category(emotion):
    """Get category (positive/neutral/negative/special) for an emotion"""
    emotion_lower = emotion.lower()
    for category, emotions in EMOTION_CATEGORIES.items():
        if emotion_lower in emotions:
            return category
    return 'neutral'
