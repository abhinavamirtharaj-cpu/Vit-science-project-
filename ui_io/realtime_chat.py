"""
realtime_chat.py
WhatsApp-style real-time chat with WebSocket support and sentiment analysis.

Features:
- Real-time messaging with WebSockets
- Contact-based persistent messaging
- Sentiment analysis on all messages
- Left/right message alignment (like WhatsApp)
- Offline message support
- Message persistence with history loading
"""
import os
import sys
from flask import Flask, render_template, request, session
from flask_socketio import SocketIO, emit
from datetime import datetime
import secrets

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core_analysis.chat_service import process_user_message
from ui_io.storage import append_message, get_history

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', secrets.token_hex(32))
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# Store online users
online_users = {}  # {user_id: sid}
sid_to_user = {}   # {sid: user_id}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/chat')
def chat():
    return render_template('chat.html')



@socketio.on('connect')
def handle_connect():
    """Handle new user connection"""
    print(f'Client connected: {request.sid}')
    emit('connected', {'sid': request.sid})


@socketio.on('disconnect')
def handle_disconnect():
    """Handle user disconnection"""
    sid = request.sid
    
    if sid in sid_to_user:
        user_id = sid_to_user[sid]
        
        # Remove from online users
        if user_id in online_users:
            del online_users[user_id]
        
        del sid_to_user[sid]
        
        # Notify other users that this user went offline
        emit('user_status', {
            'user_id': user_id,
            'online': False
        }, broadcast=True)
        
        print(f'User {user_id} disconnected')


@socketio.on('register_user')
def handle_register_user(data):
    """Register user when they join"""
    user_id = data.get('id')
    username = data.get('name', 'Anonymous')
    sid = request.sid
    
    # Store user mappings
    online_users[user_id] = sid
    sid_to_user[sid] = user_id
    
    # Notify all users that this user is online
    emit('user_status', {
        'user_id': user_id,
        'online': True
    }, broadcast=True)
    
    print(f'User registered: {username} ({user_id})')


@socketio.on('load_messages')
def handle_load_messages(data):
    """Load message history for a contact"""
    contact_id = data.get('contact_id')
    sid = request.sid
    
    if sid not in sid_to_user:
        return
    
    user_id = sid_to_user[sid]
    
    # Load messages between these two users
    conversation_id = get_conversation_id(user_id, contact_id)
    history = get_history(conversation_id)
    
    messages = []
    if history:
        for msg in history[-50:]:  # Last 50 messages
            messages.append({
                'text': msg.get('message', ''),
                'from': msg.get('from', ''),
                'timestamp': msg.get('timestamp', ''),
                'sentiment': {
                    'category': msg.get('sentiment', {}).get('category', 'Neutral'),
                    'emoji': msg.get('sentiment', {}).get('emoji', '😐'),
                    'polarity': msg.get('sentiment', {}).get('polarity_score', 0)
                }
            })
    
    emit('messages_loaded', {'messages': messages})
    print(f'Loaded {len(messages)} messages for {user_id} with {contact_id}')


@socketio.on('send_message')
def handle_send_message(data):
    """Handle new message from user"""
    text = data.get('text', '').strip()
    to_user = data.get('to')
    from_user = data.get('from')
    
    if not text or not to_user or not from_user:
        return
    
    # Process message with sentiment analysis
    contact = {'id': to_user, 'name': to_user}
    result = process_user_message(text, contact)
    
    # Get conversation ID for storage
    conversation_id = get_conversation_id(from_user, to_user)
    
    # Save message
    message_data = {
        'from': from_user,
        'to': to_user,
        'message': text,
        'timestamp': datetime.utcnow().isoformat(),
        'sentiment': {
            'category': result['sentiment']['category'],
            'emoji': result['sentiment']['emoji'],
            'polarity': result['sentiment']['polarity_score']
        }
    }
    
    append_message(conversation_id, text, result['sentiment'])
    
    # Send confirmation to sender
    emit('message_sent', {
        'text': text,
        'sentiment': message_data['sentiment']
    })
    
    # Send to recipient if online
    if to_user in online_users:
        recipient_sid = online_users[to_user]
        emit('new_message', {
            'from': from_user,
            'text': text,
            'sentiment': message_data['sentiment'],
            'timestamp': message_data['timestamp']
        }, room=recipient_sid)
    
    print(f'Message from {from_user} to {to_user}: {text[:50]}...')


def get_conversation_id(user1, user2):
    """Generate consistent conversation ID for two users"""
    # Sort IDs to ensure same conversation ID regardless of order
    sorted_ids = sorted([user1, user2])
    return f"conv_{sorted_ids[0]}_{sorted_ids[1]}"


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    print(f"Starting WhatsApp-style Chat Server on port {port}...")
    print(f"Access at http://0.0.0.0:{port}/")
    socketio.run(app, host="0.0.0.0", port=port, debug=False)
