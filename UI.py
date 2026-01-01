"""
UI.py
Simple static Flask server for the chat UI. This file only serves the frontend files
and does not implement any server-side chat or CSV persistence logic.

Run:
  pip install flask
  python UI.py

Access in browser: http://127.0.0.1:5000/
"""
import os
from flask import Flask, send_from_directory, abort

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

if __name__ == '__main__':
    # Use Flask's built-in server for local development
    app.run(host='127.0.0.1', port=5000, debug=True)

