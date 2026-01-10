# Sentiment Color Scheme Reference

## Overview
Each sentiment category has a unique, vibrant color with gradient backgrounds and glow effects in the chat interface.

## Color Palette

### 😄 Very Positive
- **Color:** `#00E676` (Bright Green)
- **Usage:** Very happy, excited, enthusiastic messages
- **Examples:** "I absolutely love this!", "This is amazing!", "Best day ever!"
- **Visual:** Bright green gradient with green glow

### 🙂 Positive  
- **Color:** `#2196F3` (Bright Blue)
- **Usage:** Positive, good, happy messages
- **Examples:** "U r cool", "That's great", "Nice work"
- **Visual:** Bright blue gradient with blue glow

### 😐 Neutral
- **Color:** `#FFC107` (Amber/Yellow)
- **Usage:** Greetings (Hello, Hi), factual statements, neutral responses
- **Examples:** "Hello", "Okay", "I understand"
- **Visual:** Yellow gradient with dark text for readability

### ☹️ Negative
- **Color:** `#FF5722` (Deep Orange)
- **Usage:** Frustrated, annoyed, disappointed messages
- **Examples:** "This is not good", "I'm frustrated", "Not working"
- **Visual:** Orange-red gradient with orange glow

### 😠 Very Negative
- **Color:** `#E91E63` (Pink/Magenta)
- **Usage:** Angry, hate, very bad messages
- **Examples:** "This is a very bad idea!", "I hate this!", "Terrible"
- **Visual:** Pink-magenta gradient with magenta glow

### 😏 Sarcastic
- **Color:** `#9C27B0` (Purple)
- **Usage:** Sarcastic or ironic statements
- **Examples:** "Oh great, another problem", "Yeah right", "Fantastic..."
- **Visual:** Purple gradient with purple glow

## Visual Features

All sentiment message bubbles include:
- **Gradient Background:** 135° angle for depth
- **Left Border:** 4px solid line in sentiment color
- **Glow Shadow:** Colored shadow matching sentiment (16px blur, 40% opacity)
- **Smooth Transitions:** 300ms ease for all effects
- **Hover Effects:** Slight elevation on sentiment badge hover

## Special Cases

### Neutral Text Color
Neutral (yellow) messages use **dark text (#1a1a1a)** instead of white for better readability against the bright yellow background.

### Sentiment Badge
- Small badge displaying emoji + category name
- Semi-transparent background with border
- Tooltip on hover showing full sentiment description
- Uppercase text with increased letter spacing

## Implementation

Colors are applied dynamically via:
1. Backend sets `color` attribute in sentiment data
2. Frontend applies `data-sentiment-color` attribute to message bubble
3. CSS matches attribute selectors for styling

Example:
```html
<div class="msg sent" data-sentiment-color="#00E676" data-sentiment-category="Very Positive">
  <div class="text">I absolutely love this!</div>
  <span class="sentiment-badge">😄 VERY POSITIVE</span>
</div>
```

## Files Modified

- `/workspaces/SCIVIT-Draft/core_analysis/chat_service.py` - Color mapping
- `/workspaces/SCIVIT-Draft/ui_io/styles.css` - CSS styling rules
- `/workspaces/SCIVIT-Draft/interface_js/script.js` - Dynamic attribute application
