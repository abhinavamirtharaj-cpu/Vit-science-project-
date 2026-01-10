# Emotion Detection System

## Overview
The system now supports **40+ distinct emotions** with unique colors, instead of just 6 sentiment categories. Each emotion has its own color, emoji, and visual styling.

## Supported Emotions

### Positive Emotions (14)
| Emotion | Color | Emoji | Description |
|---------|-------|-------|-------------|
| joy | `#00E676` (Bright green) | 😄 | Pure happiness and delight |
| happiness | `#76FF03` (Lime green) | 😊 | General state of being happy |
| love | `#FF4081` (Pink) | ❤️ | Affection and love |
| excitement | `#FFD600` (Bright yellow) | 🤩 | High energy enthusiasm |
| enthusiasm | `#FFC400` (Amber) | 🎉 | Passionate interest |
| fun | `#FF6E40` (Deep orange) | 😆 | Playful enjoyment |
| admiration | `#7C4DFF` (Deep purple) | 😍 | Respect and appreciation |
| amusement | `#FFAB40` (Orange) | 😂 | Finding something funny |
| approval | `#69F0AE` (Light green) | 👍 | Agreement and support |
| caring | `#F06292` (Light pink) | 🤗 | Compassion and concern |
| gratitude | `#4FC3F7` (Light blue) | 🙏 | Thankfulness |
| relief | `#81C784` (Medium green) | 😌 | Feeling of release |
| pride | `#9575CD` (Medium purple) | 😤 | Sense of achievement |
| optimism | `#FFD54F` (Light yellow) | ✨ | Hopeful outlook |

### Neutral Emotions (5)
| Emotion | Color | Emoji | Description |
|---------|-------|-------|-------------|
| neutral | `#90A4AE` (Blue gray) | 😐 | No strong emotion |
| surprise | `#FFEB3B` (Yellow) | 😲 | Unexpected event |
| realization | `#26C6DA` (Cyan) | 💡 | Understanding something |
| confusion | `#B0BEC5` (Light gray) | 😕 | Lack of understanding |
| curiosity | `#4DD0E1` (Light cyan) | 🤔 | Desire to know |

### Negative Emotions (15)
| Emotion | Color | Emoji | Description |
|---------|-------|-------|-------------|
| anger | `#F44336` (Red) | 😠 | Strong displeasure |
| annoyance | `#FF7043` (Deep orange) | 😒 | Mild irritation |
| disapproval | `#FF5252` (Red accent) | 👎 | Disagreement |
| sadness | `#5C6BC0` (Indigo) | 😢 | Sorrow and unhappiness |
| fear | `#7E57C2` (Deep purple) | 😨 | Afraid or scared |
| worry | `#AB47BC` (Purple) | 😟 | Anxious concern |
| hate | `#D32F2F` (Dark red) | 😡 | Intense dislike |
| grief | `#512DA8` (Deep indigo) | 😭 | Deep sorrow |
| nervousness | `#BA68C8` (Light purple) | 😰 | Anxious tension |
| disgust | `#8D6E63` (Brown) | 🤢 | Revulsion |
| disappointment | `#E64A19` (Deep orange) | 😞 | Let down |
| embarrassment | `#EC407A` (Pink) | 😳 | Feeling awkward |
| shame | `#C62828` (Dark red) | 😔 | Feeling ashamed |
| guilt | `#AD1457` (Dark pink) | 😖 | Sense of wrongdoing |
| remorse | `#6A1B9A` (Dark purple) | 😣 | Deep regret |

### Special Emotions (10)
| Emotion | Color | Emoji | Description |
|---------|-------|-------|-------------|
| sarcasm | `#9C27B0` (Purple) | 😏 | Ironic/mocking |
| empathy | `#26A69A` (Teal) | 🫂 | Understanding others' feelings |
| anxiety | `#5E35B1` (Deep purple) | 😧 | Persistent worry |
| depression | `#455A64` (Dark gray) | 😶 | Persistent sadness |
| stress | `#FF6F00` (Dark orange) | 😫 | Mental/emotional strain |
| frustration | `#EF5350` (Light red) | 😤 | Blocked from goals |
| jealousy | `#388E3C` (Dark green) | 😒 | Envious feelings |
| loneliness | `#546E7A` (Gray blue) | 🥺 | Feeling alone |
| boredom | `#78909C` (Medium gray) | 😑 | Lack of interest |

## How It Works

### 1. Emotion Detection
The system uses keyword matching + sentiment analysis to detect emotions:

```python
from emotion_analyzer import analyze_emotion

result = analyze_emotion("I'm so happy today!")
# Returns: {'emotion': 'joy', 'polarity': 0.8, 'category': 'positive'}
```

### 2. Color Assignment
Each emotion has a unique color defined in `emotion_colors.py`:

```python
from emotion_colors import get_emotion_color

color = get_emotion_color('joy')
# Returns: '#00E676'
```

### 3. UI Rendering
Messages are displayed with emotion-specific styling:
- **Gradient background** with the emotion's color
- **Left border** in the emotion color
- **Colored glow shadow** for depth
- **Dark text** on light backgrounds (yellow emotions)

## Files

### Core Files
- **emotion_colors.py** - Color palette and emoji mappings for all emotions
- **emotion_analyzer.py** - Emotion detection using keywords and TextBlob
- **train_with_emotions.py** - Training pipeline for emotion-labeled data
- **generate_emotion_css.py** - CSS generator for all emotions

### Updated Files
- **core_analysis/chat_service.py** - Now supports emotion mode
- **ui_io/styles.css** - Contains CSS for all 40+ emotions
- **data/emotion_training.csv** - Training data with emotion labels

## Usage

### Testing Emotions
Try these messages to see different emotions:

```
"I'm so happy!" → joy (bright green)
"This is terrible" → sadness (indigo)
"I'm furious!" → anger (red)
"I'm scared" → fear (deep purple)
"Wow amazing!" → excitement (yellow)
"Thank you!" → gratitude (light blue)
"I'm worried" → worry (purple)
"So frustrating" → frustration (light red)
"I feel lonely" → loneliness (gray blue)
"You're the best!" → love (pink)
```

### Training with Emotions
To add more emotion-labeled data:

1. Create CSV with columns: `contact_id`, `message`, `dir`, `emotion`
2. Place in `data/` directory
3. Run: `python train_with_emotions.py`

### Switching Modes
The system automatically uses emotion mode when `emotion_analyzer.py` is available. To disable:
- Set `EMOTION_MODE = False` in `chat_service.py`

## CSS Styling
Each emotion gets dynamic CSS with gradients:

```css
/* Example: Joy */
.msg.sent[data-sentiment-color="#00E676"]{
  background:linear-gradient(135deg, rgba(0, 230, 118, 0.85), rgba(0, 200, 88, 0.85));
  border-left:4px solid #00E676;
  box-shadow:0 4px 16px rgba(0, 230, 118, 0.4);
}
```

## Benefits
- **More precise** - 40+ emotions vs 6 categories
- **Better UX** - Distinct colors make emotions instantly recognizable
- **Richer data** - Detailed emotion tracking for analysis
- **Scalable** - Easy to add new emotions

## Next Steps
1. Refresh browser to see new CSS
2. Type messages to test emotion detection
3. Add custom emotions to `emotion_colors.py`
4. Train with more emotion-labeled data
