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
waiting_user = None  # Single user waiting to be paired: {'sid': sid, 'username': username}
active_rooms = {}  # {room_id: {'user1': {'sid': sid, 'username': username}, 'user2': {...}}}
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
    global waiting_user
    sid = request.sid
    
    # Check if disconnecting user was waiting
    if waiting_user and waiting_user['sid'] == sid:
        waiting_user = None
        print(f'Waiting user disconnected: {sid}')
        return
    
    # Leave room if in one
    if sid in user_rooms:
        room_id = user_rooms[sid]
        leave_room(room_id)
        
        # Notify partner
        if room_id in active_rooms:
            room_data = active_rooms[room_id]
            partner_sid = None
            disconnected_username = ''
            
            if room_data['user1']['sid'] == sid:
                partner_sid = room_data['user2']['sid']
                disconnected_username = room_data['user1']['username']
            elif room_data['user2']['sid'] == sid:
                partner_sid = room_data['user1']['sid']
                disconnected_username = room_data['user2']['username']
            
            if partner_sid:
                emit('partner_left', {
                    'username': disconnected_username
                }, room=partner_sid)
                
                # Remove partner from room tracking
                if partner_sid in user_rooms:
                    del user_rooms[partner_sid]
            
            # Clean up room
            del active_rooms[room_id]
        
        del user_rooms[sid]
    
    print(f'Client disconnected: {sid}')


@socketio.on('find_partner')
def handle_find_partner(data):
    """Match user with next available partner"""
    global waiting_user
    username = data.get('username', 'Anonymous')
    sid = request.sid
    
    # Check if someone is already waiting
    if waiting_user and waiting_user['sid'] != sid:
        # Pair them together
        room_id = f"room_{waiting_user['sid'][:8]}_{sid[:8]}"
        
        # Create room with both users
        active_rooms[room_id] = {
            'user1': waiting_user,
            'user2': {'sid': sid, 'username': username}
        }
        
        # Join both to room
        user_rooms[waiting_user['sid']] = room_id
        user_rooms[sid] = room_id
        
        join_room(room_id, sid=waiting_user['sid'])
        join_room(room_id, sid=sid)
        
        # Notify both users they're paired
        emit('paired', {
            'room_id': room_id,
            'partner_name': username
        }, room=waiting_user['sid'])
        
        emit('paired', {
            'room_id': room_id,
            'partner_name': waiting_user['username']
        })
        
        # Send chat history
        contact = {'id': room_id, 'name': room_id}
        history = get_history(room_id)
        if history:
            emit('chat_history', {'messages': history[-50:]}, room=room_id)
        
        print(f'Paired {waiting_user["username"]} with {username} in room {room_id}')
        
        # Clear waiting user
        waiting_user = None
    else:
        # No one waiting, this user becomes the waiting user
        waiting_user = {'sid': sid, 'username': username}
        user_rooms[sid] = None  # Not in a room yet
        emit('waiting')
        print(f'User {username} ({sid}) is waiting for a partner')


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
