"""SQLite storage layer for messages and contacts"""
import sqlite3
from pathlib import Path
import json
from typing import Optional, List, Dict, Any
from datetime import datetime
import shutil
import logging

from config import DB_PATH, BACKUP_DIR, CONTACTS_JSON

logger = logging.getLogger("sean.storage")


class Storage:
    def __init__(self, db_path: Path = DB_PATH):
        self.db_path = db_path
        self.conn = sqlite3.connect(str(self.db_path), check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self._init_db()

    def _init_db(self):
        c = self.conn.cursor()
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS contacts(
                name TEXT PRIMARY KEY,
                public_key BLOB NOT NULL,
                private_key_encrypted BLOB,
                created_date TEXT,
                last_seen TEXT
            )
            """
        )
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS messages(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                packet_id TEXT UNIQUE,
                contact_name TEXT,
                direction TEXT,
                encrypted_packet TEXT,
                timestamp TEXT,
                status TEXT,
                size_bytes INTEGER
            )
            """
        )
        self.conn.commit()
        BACKUP_DIR.mkdir(parents=True, exist_ok=True)
        if not CONTACTS_JSON.exists():
            CONTACTS_JSON.write_text("[]")

    # Contacts
    def add_contact(self, name: str, public_key: bytes, private_key_encrypted: Optional[bytes] = None):
        now = datetime.utcnow().isoformat()
        c = self.conn.cursor()
        c.execute(
            "INSERT OR REPLACE INTO contacts (name, public_key, private_key_encrypted, created_date, last_seen) VALUES (?, ?, ?, ?, ?)",
            (name, public_key, private_key_encrypted, now, now),
        )
        self.conn.commit()
        self._sync_contacts_json()

    def get_contact(self, name: str) -> Optional[sqlite3.Row]:
        c = self.conn.cursor()
        c.execute("SELECT * FROM contacts WHERE name=?", (name,))
        return c.fetchone()

    def list_contacts(self) -> List[sqlite3.Row]:
        c = self.conn.cursor()
        c.execute("SELECT * FROM contacts")
        return c.fetchall()

    def delete_contact(self, name: str):
        c = self.conn.cursor()
        c.execute("DELETE FROM contacts WHERE name=?", (name,))
        c.execute("DELETE FROM messages WHERE contact_name=?", (name,))
        self.conn.commit()
        self._sync_contacts_json()

    def _sync_contacts_json(self):
        # dump public keys for backup
        c = self.conn.cursor()
        c.execute("SELECT name, public_key, created_date, last_seen FROM contacts")
        rows = c.fetchall()
        arr = []
        for r in rows:
            arr.append({
                "name": r[0],
                "public_key": r[1].decode() if isinstance(r[1], (bytes, bytearray)) else r[1],
                "created_date": r[2],
                "last_seen": r[3],
            })
        CONTACTS_JSON.write_text(json.dumps(arr, indent=2))

    # Messages
    def add_message(self, packet_id: str, contact_name: str, direction: str, encrypted_packet: str, timestamp: str, status: str, size_bytes: int):
        c = self.conn.cursor()
        try:
            c.execute(
                "INSERT INTO messages (packet_id, contact_name, direction, encrypted_packet, timestamp, status, size_bytes) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (packet_id, contact_name, direction, encrypted_packet, timestamp, status, size_bytes),
            )
            self.conn.commit()
        except sqlite3.IntegrityError:
            logger.warning("Duplicate packet_id %s skipped", packet_id)

    def get_history(self, contact_name: str, search: Optional[str] = None) -> List[Dict[str, Any]]:
        c = self.conn.cursor()
        if search:
            q = f"%{search}%"
            c.execute("SELECT * FROM messages WHERE contact_name=? AND encrypted_packet LIKE ? ORDER BY id", (contact_name, q))
        else:
            c.execute("SELECT * FROM messages WHERE contact_name=? ORDER BY id", (contact_name,))
        rows = c.fetchall()
        return [dict(r) for r in rows]

    def clear_history(self, contact_name: str):
        c = self.conn.cursor()
        c.execute("DELETE FROM messages WHERE contact_name=?", (contact_name,))
        self.conn.commit()

    def count_messages(self) -> int:
        c = self.conn.cursor()
        c.execute("SELECT COUNT(*) FROM messages")
        return c.fetchone()[0]

    def update_message_status(self, packet_id: str, status: str):
        c = self.conn.cursor()
        c.execute("UPDATE messages SET status=? WHERE packet_id=?", (status, packet_id))
        self.conn.commit()

    def backup_db(self):
        stamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        dest = BACKUP_DIR / f"sean_{stamp}.db"
        self.conn.commit()
        shutil.copyfile(self.db_path, dest)
        logger.info("DB backup created: %s", dest)
        return dest

    def restore_db(self, path: Path):
        self.conn.close()
        shutil.copyfile(path, self.db_path)
        self.conn = sqlite3.connect(str(self.db_path), check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        logger.info("DB restored from %s", path)

    def close(self):
        self.conn.commit()
        self.conn.close()
