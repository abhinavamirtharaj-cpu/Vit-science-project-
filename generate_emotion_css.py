"""
generate_emotion_css.py
Generate CSS rules for all emotion colors and append to styles.css
"""

from emotion_colors import EMOTION_COLORS

def generate_emotion_css():
    """Generate CSS for all emotions"""
    css_lines = []
    
    css_lines.append("\n/* ========================================")
    css_lines.append("   EMOTION-SPECIFIC MESSAGE BUBBLE STYLES")
    css_lines.append("   Generated dynamically for 40+ emotions")
    css_lines.append("   ======================================== */\n")
    
    for emotion, color in sorted(EMOTION_COLORS.items()):
        # Convert hex to RGB for gradient
        hex_color = color.lstrip('#')
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        
        # Create gradient with slight variation (darker)
        r2 = max(0, r - 30)
        g2 = max(0, g - 30)
        b2 = max(0, b - 30)
        
        css_lines.append(f"/* {emotion.title()} - {color} */")
        css_lines.append(f'.msg.sent[data-sentiment-color="{color}"]{{')
        css_lines.append(f'  background:linear-gradient(135deg, rgba({r}, {g}, {b}, 0.85), rgba({r2}, {g2}, {b2}, 0.85));')
        css_lines.append(f'  border-left:4px solid {color};')
        css_lines.append(f'  box-shadow:0 4px 16px rgba({r}, {g}, {b}, 0.4);')
        
        # Special handling for light colors (yellow tones) - use dark text
        if (r > 200 and g > 200) or (g > 220 and r > 200):
            css_lines.append(f'  color:#1a1a1a !important;')
        
        css_lines.append('}')
        css_lines.append('')
    
    css_lines.append(f"/* Total emotions supported: {len(EMOTION_COLORS)} */\n")
    
    return '\n'.join(css_lines)

def append_to_styles_css():
    """Append emotion CSS to styles.css"""
    styles_path = 'ui_io/styles.css'
    
    # Read current file
    with open(styles_path, 'r') as f:
        content = f.read()
    
    # Check if emotion styles already exist
    if 'EMOTION-SPECIFIC MESSAGE BUBBLE STYLES' in content:
        print("✅ Emotion styles already exist in styles.css")
        return
    
    # Generate new CSS
    emotion_css = generate_emotion_css()
    
    # Append to file
    with open(styles_path, 'a') as f:
        f.write(emotion_css)
    
    print(f"✅ Added CSS for {len(EMOTION_COLORS)} emotions to {styles_path}")
    print(f"   Total file size: {len(content) + len(emotion_css)} characters")

if __name__ == '__main__':
    print("="*60)
    print("GENERATING EMOTION CSS")
    print("="*60)
    
    append_to_styles_css()
    
    print("\n" + "="*60)
    print("✅ COMPLETE!")
    print("="*60)
