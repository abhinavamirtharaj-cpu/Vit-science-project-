"""SEAN CLI: configuration and colors"""
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "sean.db"
CONTACTS_JSON = BASE_DIR / "contacts.json"
MASTER_KEY_FILE = BASE_DIR / "master.key"
LOG_FILE = BASE_DIR / "sean.log"
BACKUP_DIR = BASE_DIR / "backups"

# Server defaults for real-time relay (for local testing)
SERVER_HOST = "localhost"
SERVER_PORT = 8765

# ANSI colors
class Colors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"

# Message status icons
STATUS_ICONS = {
    "pending": "🟡",
    "sent": "🟢",
    "delivered": "🔵",
    "read": "⚫",
}
