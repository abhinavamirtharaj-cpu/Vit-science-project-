"""
UI.py
Flask server with sentiment analysis integration for the chat UI.

Features:
- Serves frontend files (HTML, CSS, JS)
- Provides API endpoint for sentiment analysis
- Integrates with chat_service for message processing and storage

Run:
  pip install flask textblob
  python UI.py

Access in browser: http://127.0.0.1:5000/
"""
import os
import json
from flask import Flask, send_from_directory, abort, request, jsonify
from chat_service import process_user_message, get_history

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__, static_folder=APP_ROOT, static_url_path='')


# Static file routes
@app.route('/')
def index():
    return send_from_directory(APP_ROOT, 'index.html')


@app.route('/<path:filename>')
def static_files(filename):
    file_path = os.path.join(APP_ROOT, filename)
    if os.path.exists(file_path):
        return send_from_directory(APP_ROOT, filename)
    abort(404)


# API Routes
@app.route('/api/analyze', methods=['POST'])
def analyze_message():
    """
    Endpoint to analyze a message and return sentiment data.
    
    Request JSON:
    {
        "text": "message text",
        "contact_id": "contact_id",
        "contact_name": "contact_name"
    }
    
    Response JSON:
    {
        "success": true,
        "message": {...},
        "sentiment": {...},
        "trend": "improving|declining|stable"
    }
    """
    try:
        data = request.get_json()
        text = data.get('text', '').strip()
        contact_id = data.get('contact_id', 'unknown')
        contact_name = data.get('contact_name', 'User')
        
        if not text:
            return jsonify({"success": False, "error": "Empty message"}), 400
        
        contact = {'id': contact_id, 'name': contact_name}
        result = process_user_message(text, contact)
        
        return jsonify({
            "success": True,
            "message": result['message'],
            "sentiment": {
                "category": result['sentiment']['category'],
                "emoji": result['sentiment']['emoji'],
                "description": result['sentiment']['description'],
                "polarity": result['sentiment']['polarity_score'],
                "color": result['sentiment']['color']
            },
            "trend": result['trend']
        }), 200
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


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
        history = get_history(contact_id)
        return jsonify({
            "success": True,
            "messages": history
        }), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "ok", "service": "chat-sentiment-analyzer"}), 200


if __name__ == '__main__':
    # Use Flask's built-in server for local development
    app.run(host='127.0.0.1', port=5000, debug=True)


