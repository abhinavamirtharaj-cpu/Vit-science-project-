import os
import sys

# Add root directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the real-time chat app instead
from ui_io.realtime_chat import app, socketio

if __name__ == "__main__":
    print("Starting Real-Time Chat Application with Sentiment Analysis...")
    # Use PORT environment variable for cloud hosting (Render, Heroku, etc.)
    port = int(os.environ.get("PORT", 5000))
    print(f"Access at http://0.0.0.0:{port}/")
    socketio.run(app, host="0.0.0.0", port=port, debug=False)
