"""
realtime_chat.py
Real-time two-person chat with WebSocket support and sentiment analysis.

Features:
- Real-time messaging with WebSockets
- Room-based chat (2 users per room)
- Sentiment analysis on all messages
- Left/right message alignment (like WhatsApp)
- Message persistence
"""
import os
import sys
from flask import Flask, render_template, request, session
from flask_socketio import SocketIO, emit, join_room, leave_room
from datetime import datetime
import secrets

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core_analysis.chat_service import process_user_message
from ui_io.storage import get_history

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', secrets.token_hex(32))
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# Store active rooms and users
active_rooms = {}  # {room_id: [user1_sid, user2_sid]}
user_names = {}    # {sid: username}
user_rooms = {}    # {sid: room_id}


@app.route('/')
def index():
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
    
    # Leave room if in one
    if sid in user_rooms:
        room_id = user_rooms[sid]
        leave_room(room_id)
        
        # Remove from active rooms
        if room_id in active_rooms and sid in active_rooms[room_id]:
            active_rooms[room_id].remove(sid)
            
            # Notify other user
            if active_rooms[room_id]:
                emit('user_left', {
                    'username': user_names.get(sid, 'Unknown')
                }, room=room_id)
            else:
                del active_rooms[room_id]
        
        del user_rooms[sid]
    
    # Clean up user data
    if sid in user_names:
        del user_names[sid]
    
    print(f'Client disconnected: {sid}')


@socketio.on('join_room')
def handle_join_room(data):
    """Handle user joining a room"""
    room_id = data.get('room_id', 'default')
    username = data.get('username', 'Anonymous')
    sid = request.sid
    
    # Store user info
    user_names[sid] = username
    user_rooms[sid] = room_id
    
    # Initialize room if doesn't exist
    if room_id not in active_rooms:
        active_rooms[room_id] = []
    
    # Check if room is full (max 2 users)
    if len(active_rooms[room_id]) >= 2 and sid not in active_rooms[room_id]:
        emit('room_full', {'error': 'Room is full (max 2 users)'})
        return
    
    # Join the room
    join_room(room_id)
    if sid not in active_rooms[room_id]:
        active_rooms[room_id].append(sid)
    
    # Send room info to user
    emit('room_joined', {
        'room_id': room_id,
        'username': username,
        'users_count': len(active_rooms[room_id])
    })
    
    # Notify others in room
    emit('user_joined', {
        'username': username,
        'users_count': len(active_rooms[room_id])
    }, room=room_id, include_self=False)
    
    # Send chat history
    contact = {'id': room_id, 'name': room_id}
    history = get_history(room_id)
    emit('chat_history', {'messages': history[-50:]})  # Last 50 messages
    
    print(f'User {username} ({sid}) joined room {room_id}')


@socketio.on('send_message')
def handle_send_message(data):
    """Handle new message from user"""
    text = data.get('text', '').strip()
    room_id = data.get('room_id', 'default')
    sid = request.sid
    username = user_names.get(sid, 'Anonymous')
    
    if not text:
        return
    
    # Process message with sentiment analysis
    contact = {'id': room_id, 'name': room_id}
    result = process_user_message(text, contact)
    
    # Prepare message data
    message_data = {
        'id': datetime.utcnow().isoformat(),
        'text': text,
        'username': username,
        'sender_sid': sid,
        'timestamp': datetime.utcnow().isoformat(),
        'sentiment': {
            'category': result['sentiment']['category'],
            'emoji': result['sentiment']['emoji'],
            'polarity': result['sentiment']['polarity_score'],
            'color': result['sentiment']['color'],
            'description': result['sentiment']['description']
        }
    }
    
    # Broadcast to room
    emit('new_message', message_data, room=room_id)
    
    print(f'Message from {username} in {room_id}: {text[:50]}...')


@socketio.on('typing')
def handle_typing(data):
    """Handle typing indicator"""
    room_id = data.get('room_id')
    username = user_names.get(request.sid, 'Anonymous')
    
    emit('user_typing', {
        'username': username,
        'is_typing': data.get('is_typing', False)
    }, room=room_id, include_self=False)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    print(f"Starting Real-time Chat Server on port {port}...")
    print(f"Access at http://0.0.0.0:{port}/")
    socketio.run(app, host="0.0.0.0", port=port, debug=False)
