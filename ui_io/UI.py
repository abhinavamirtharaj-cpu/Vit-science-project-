"""
UI.py - Real-time two-person chat with sentiment analysis
Flask server with WebSocket support for real-time messaging between two devices.

Features:
- Real-time WebSocket communication
- Two-person messaging (messages displayed left/right based on sender)
- Common room "LOCAL" for both users
- Sentiment analysis on all messages
- Message history persistence

Run:
  pip install flask flask-socketio python-socketio textblob
  python UI.py

Access in browser: http://127.0.0.1:5000/
Access from another device: http://YOUR_IP_ADDRESS:5000/
"""
import os
import sys
import json
from flask import Flask, send_from_directory, abort, request, jsonify
from flask_socketio import SocketIO, emit, join_room, leave_room
from datetime import datetime

# Add parent directory to path to find other modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core_analysis.chat_service import process_user_message, get_history
from ui_io.storage import append_message

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(APP_ROOT)
INTERFACE_JS_DIR = os.path.join(PROJECT_ROOT, 'interface_js')

# Disable default static file handling to allow custom routing for interface_js
app = Flask(__name__, static_folder=None)
app.config['SECRET_KEY'] = 'vit-science-project-secret-key-2026'
socketio = SocketIO(app, cors_allowed_origins="*")

# Store active users and their sessions
active_sessions = {}


# Static file routes
@app.route('/')
def index():
    return send_from_directory(APP_ROOT, 'index.html')


@app.route('/<path:filename>')
def static_files(filename):
    # Check ui_io folder
    file_path = os.path.join(APP_ROOT, filename)
    if os.path.exists(file_path):
        return send_from_directory(APP_ROOT, filename)
    
    # Check interface_js folder (for script.js)
    js_path = os.path.join(INTERFACE_JS_DIR, filename)
    if os.path.exists(js_path):
        return send_from_directory(INTERFACE_JS_DIR, filename)
        
    abort(404)


# WebSocket Events
@socketio.on('join_chat')
def handle_join(data):
    """
    User joins the LOCAL chat room.
    
    Expected data:
    {
        "username": "User's name"
    }
    """
    username = data.get('username', 'Anonymous')
    room = 'LOCAL'  # Common room name for both users
    
    join_room(room)
    active_sessions[request.sid] = {'username': username, 'room': room}
    
    print(f"[JOIN] {username} joined room {room}")
    
    # Notify others that user joined
    emit('user_joined', {
        'username': username,
        'message': f'{username} joined the chat'
    }, room=room, skip_sid=request.sid)
    
    # Send chat history to the joining user
    try:
        messages = get_history('LOCAL')
        formatted_messages = []
        
        for msg in messages:
            formatted_messages.append({
                'sender': msg.get('sender', 'Unknown'),
                'text': msg.get('text', ''),
                'timestamp': msg.get('iso', datetime.now().isoformat()),
                'sentiment': {
                    'category': msg.get('sentiment_category', 'Neutral'),
                    'emoji': msg.get('sentiment_emoji', '😐'),
                    'color': msg.get('color_hex', '#9E9E9E'),
                    'polarity': msg.get('sentiment_polarity', 0)
                }
            })
        
        emit('chat_history', {'messages': formatted_messages})
    except Exception as e:
        print(f"[ERROR] Loading history: {e}")
        emit('chat_history', {'messages': []})


@socketio.on('send_message')
def handle_message(data):
    """
    Process and broadcast message to all users in the room.
    
    Expected data:
    {
        "text": "message content"
    }
    """
    try:
        session = active_sessions.get(request.sid)
        if not session:
            emit('error', {'message': 'Not connected to chat'})
            return
        
        username = session['username']
        room = session['room']
        text = data.get('text', '').strip()
        
        if not text:
            return
        
        print(f"[MESSAGE] {username}: {text}")
        
        # Process message with sentiment analysis
        contact = {'id': 'LOCAL', 'name': room}
        result = process_user_message(text, contact)
        
        # Prepare message data for storage with sender info
        now = datetime.now()
        message_data = {
            'dir': 'sent',
            'iso': now.isoformat(),
            'date': now.strftime('%Y-%m-%d'),
            'time': now.strftime('%H:%M'),
            'text': text,
            'sender': username,  # Add sender field
            'sentiment_polarity': result['sentiment']['polarity_score'],
            'sentiment_category': result['sentiment']['category'],
            'sentiment_emoji': result['sentiment']['emoji'],
            'color_hex': result['sentiment']['color']
        }
        
        # Store message with sender info
        append_message(contact, message_data)
        
        # Broadcast to all users in room (including sender)
        emit('new_message', {
            'sender': username,
            'text': text,
            'timestamp': now.isoformat(),
            'sentiment': {
                'category': result['sentiment']['category'],
                'emoji': result['sentiment']['emoji'],
                'color': result['sentiment']['color'],
                'polarity': result['sentiment']['polarity_score']
            },
            'trend': result.get('trend', 'stable')
        }, room=room)
        
    except Exception as e:
        print(f"[ERROR] Processing message: {e}")
        emit('error', {'message': str(e)})


@socketio.on('disconnect')
def handle_disconnect():
    """
    User disconnected from chat.
    """
    session = active_sessions.pop(request.sid, None)
    if session:
        print(f"[DISCONNECT] {session['username']} left")
        emit('user_left', {
            'username': session['username'],
            'message': f"{session['username']} left the chat"
        }, room=session['room'])
        leave_room(session['room'])


# REST API Routes (for backward compatibility)
@app.route('/api/history/<contact_id>', methods=['GET'])
def get_chat_history(contact_id):
    """
    Endpoint to retrieve chat history for a contact.
    
    Response JSON:
    {
        "success": true,
        "messages": [...]
    }
    """
    try:
        messages = get_history(contact_id)
        return jsonify({"success": True, "messages": messages}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == '__main__':
    print("\n" + "="*50)
    print("Starting Two-Person Chat Server")
    print("="*50)
    print(f"Server running on: http://0.0.0.0:5000")
    print(f"Access locally: http://127.0.0.1:5000")
    print(f"Access from network: http://YOUR_IP_ADDRESS:5000")
    print("="*50 + "\n")
    
    socketio.run(app, debug=True, port=5000, host='0.0.0.0')