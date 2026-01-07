import os
import sys

# Add root directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ui_io.UI import app

if __name__ == "__main__":
    print("Starting Sentiment Analysis Chat Application...")
    print("Access at http://127.0.0.1:5000/")
    app.run(debug=True, port=5000)
