# Two-Person Real-Time Chat with Sentiment Analysis

## Overview

This is a **WhatsApp-style two-person messaging system** with integrated **sentiment analysis**. Messages are exchanged in real-time between two devices, with each message analyzed for emotional content.

### Key Features

- ✅ **Real-time messaging** via WebSocket (Socket.IO)
- ✅ **WhatsApp-style UI** - Your messages on the right, theirs on the left
- ✅ **Common room "LOCAL"** displayed for both users
- ✅ **Sentiment analysis** on every message with emoji indicators
- ✅ **Message history** stored in CSV format
- ✅ **Cross-device support** - works on any device with a web browser
- ✅ **Responsive design** - works on desktop, tablet, and mobile

---

## Quick Start Guide

### 1. Install Dependencies

```bash
# Navigate to project directory
cd Vit-science-project-

# Install required packages
pip install -r requirements.txt
```

### 2. Start the Server

```bash
# Run the Flask server
python ui_io/UI.py
```

You should see:
```
==================================================
Starting Two-Person Chat Server
==================================================
Server running on: http://0.0.0.0:5000
Access locally: http://127.0.0.1:5000
Access from network: http://YOUR_IP_ADDRESS:5000
==================================================
```

### 3. Access from Two Devices

#### Device 1 (Same computer):
- Open browser: `http://127.0.0.1:5000`
- Enter your name (e.g., "Alice")
- Click "Join Chat"

#### Device 2 (Another device on same network):
- Find your server's IP address:
  - **Windows**: `ipconfig` (look for IPv4 Address)
  - **Mac/Linux**: `ifconfig` or `ip addr` (look for inet)
- Open browser: `http://YOUR_IP_ADDRESS:5000`
- Enter your name (e.g., "Bob")
- Click "Join Chat"

### 4. Start Chatting!

- Type messages and press Enter to send
- Your messages appear on the **right side** (green)
- Other person's messages appear on the **left side** (gray)
- Each message shows sentiment emoji and category
- All sentiment algorithms run automatically

---

## System Architecture

### Backend Components

```
ui_io/
├── UI.py              # Flask + WebSocket server
├── storage.py         # CSV message persistence
├── index.html         # Chat interface
├── styles.css         # WhatsApp-style UI
└── chat_history_global.csv  # Message storage

interface_js/
└── script.js          # WebSocket client & UI logic

core_analysis/
├── chat_service.py    # Sentiment processing
├── node_1.py          # Sentiment node 1
├── node_2.py          # Sentiment node 2
└── node_3.py          # Sentiment node 3
```

### How It Works

1. **User joins**: Browser connects to server via WebSocket
2. **Username entry**: User provides name, joins "LOCAL" room
3. **Message sent**: User types message → sent to server via WebSocket
4. **Sentiment analysis**: Server analyzes message through 3-node architecture
5. **Storage**: Message + sentiment saved to CSV with sender info
6. **Broadcast**: Server sends message to all users in room (both devices)
7. **Display**: Each device displays message on appropriate side (left/right)

---

## Features in Detail

### 1. Two-Person Communication

- Messages sent from **Device 1** appear on:
  - **Right side** on Device 1 (you)
  - **Left side** on Device 2 (them)

- Messages sent from **Device 2** appear on:
  - **Left side** on Device 1 (them)
  - **Right side** on Device 2 (you)

### 2. Common "LOCAL" Room

- Both users see **"LOCAL"** at the top of the chat
- Below the room name, each user sees their own username: "You: [Name]"
- This creates a shared space while maintaining individual identity

### 3. Sentiment Analysis

Every message is analyzed for sentiment:

| Category | Emoji | Color | Score Range |
|----------|-------|-------|-------------|
| Very Positive | 🤩 | Green | 0.5 to 1.0 |
| Positive | 🙂 | Cyan | 0.1 to 0.5 |
| Neutral | 😐 | Yellow | -0.1 to 0.1 |
| Negative | 🙁 | Red | -0.5 to -0.1 |
| Very Negative | 😠 | Purple | -1.0 to -0.5 |
| Sarcastic | 🙃 | Blue | Special detection |

### 4. Message Persistence

All messages are stored in `chat_history_global.csv` with:
- Timestamp
- Sender name
- Message content
- Sentiment scores
- Category and emoji

---

## Network Setup

### Same WiFi Network (Recommended)

1. Connect both devices to the same WiFi
2. Start server on one device
3. Find server's IP address
4. Access from second device using `http://IP_ADDRESS:5000`

### Port Forwarding (Advanced)

For access across different networks:

1. Configure router port forwarding:
   - External Port: 5000
   - Internal Port: 5000
   - Internal IP: Your server's IP

2. Access using public IP:
   - Find public IP: `curl ifconfig.me`
   - Access: `http://PUBLIC_IP:5000`

**Security Note**: Use HTTPS and authentication for production deployments.

---

## Troubleshooting

### Issue: "Connection error. Please refresh."

**Solution**:
- Check if server is running: Look for Flask output in terminal
- Verify IP address is correct
- Ensure firewall allows port 5000
- Try `http://` instead of `https://`

### Issue: Messages not appearing in real-time

**Solution**:
- Refresh both browsers
- Check browser console for WebSocket errors (F12)
- Verify both users joined the same room ("LOCAL")
- Restart the server

### Issue: "Not connected to server"

**Solution**:
- Server may have crashed - check terminal for errors
- WebSocket connection lost - refresh page
- Check network connectivity

### Issue: Sentiment not showing

**Solution**:
- Ensure TextBlob is installed: `pip install textblob`
- Download NLTK data: `python -m textblob.download_corpora`
- Check `core_analysis/` modules are present

---

## Customization

### Change Room Name

In `interface_js/script.js`, line 5:
```javascript
const ROOM_NAME = 'LOCAL';  // Change to your preferred name
```

In `ui_io/index.html`, line 32:
```html
<strong id="chat-room-name">LOCAL</strong>  <!-- Change display name -->
```

### Modify Color Scheme

In `ui_io/styles.css`, lines 10-20:
```css
:root {
  --bg-dark: #0d1117;           /* Background color */
  --accent-green: #10b981;      /* Primary accent */
  --message-right-bg: #10b981;  /* Your messages */
  --message-left-bg: #1f2937;   /* Their messages */
}
```

### Add More Users (Multi-person Chat)

The current system is optimized for two people, but can support more:

1. Remove the "two-person" restriction in UI.py
2. Update UI to show multiple users
3. Consider adding user avatars and typing indicators

---

## API Reference

### WebSocket Events

#### Client → Server

```javascript
// Join chat room
socket.emit('join_chat', { username: 'Alice' });

// Send message
socket.emit('send_message', { text: 'Hello!' });
```

#### Server → Client

```javascript
// Chat history on join
socket.on('chat_history', (data) => {
  // data.messages = array of message objects
});

// New message broadcast
socket.on('new_message', (data) => {
  // data: { sender, text, timestamp, sentiment }
});

// User joined notification
socket.on('user_joined', (data) => {
  // data: { username, message }
});

// User left notification
socket.on('user_left', (data) => {
  // data: { username, message }
});
```

---

## Technology Stack

- **Backend**: Python 3.8+, Flask, Flask-SocketIO
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **WebSocket**: Socket.IO 4.5+
- **NLP**: TextBlob, NLTK
- **Storage**: CSV (pandas-compatible)
- **Styling**: Custom CSS (WhatsApp-inspired)

---

## Credits

Developed by **CipherCodes** team for VIT Science Project.

### Contributors
- Architecture & Backend: Core Analysis Team
- Sentiment Intelligence: NLP Processing Unit
- UI/UX Design: Interface Alchemists
- Storage & History: Contextual Memory Squad

---

## License

© 2026 SEAN - VIT Science Project

---

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review console logs (F12 in browser)
3. Verify all dependencies are installed
4. Ensure both devices are on the same network

Happy chatting! 💬✨