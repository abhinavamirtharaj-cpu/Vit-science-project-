import os
import sys

# Add root directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ui_io.UI import app

if __name__ == "__main__":
    print("Starting Sentiment Analysis Chat Application...")
    # Use PORT environment variable for cloud hosting (Render, Heroku, etc.)
    port = int(os.environ.get("PORT", 5000))
    # Disable debug mode in production
    debug = os.environ.get("FLASK_ENV") != "production"
    print(f"Access at http://0.0.0.0:{port}/")
    app.run(host="0.0.0.0", debug=debug, port=port)
