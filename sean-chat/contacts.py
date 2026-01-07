"""Contact management: add/list/delete + key backup"""
from typing import Optional, Dict
from crypto import generate_rsa_keypair, encrypt_private_pem, decrypt_private_pem
from storage import Storage
from utils import now_ts
from config import CONTACTS_JSON
import json
import logging

logger = logging.getLogger("sean.contacts")

storage = Storage()


def add_contact(name: str, make_keys: bool = True) -> Dict[str, str]:
    """Add a contact. If make_keys True: generate keys for this contact (for simulation/local)."""
    name = name.strip()
    if make_keys:
        public_pem, private_pem = generate_rsa_keypair()
        priv_enc = encrypt_private_pem(private_pem)
    else:
        public_pem = b""
        priv_enc = None
    storage.add_contact(name, public_pem, priv_enc)
    logger.info("Added contact %s", name)
    return {"name": name, "public_key": public_pem.decode() if public_pem else None}


def list_contacts():
    rows = storage.list_contacts()
    out = []
    for r in rows:
        out.append({
            "name": r[0],
            "public_key": r[1].decode() if isinstance(r[1], (bytes, bytearray)) else r[1],
            "created_date": r[3],
            "last_seen": r[4],
        })
    return out


def delete_contact(name: str):
    storage.delete_contact(name)
    logger.info("Deleted contact %s", name)


def get_private_key(name: str) -> Optional[bytes]:
    row = storage.get_contact(name)
    if not row or not row[2]:
        return None
    try:
        return decrypt_private_pem(row[2])
    except Exception as e:
        logger.exception("Failed to decrypt private key for %s: %s", name, e)
        return None


def backup_contacts_json(path=None):
    # Contacts JSON is always maintained by storage; just return its path
    return CONTACTS_JSON


def import_contacts_from_json(path):
    with open(path, "r") as f:
        data = json.load(f)
    for item in data:
        name = item.get("name")
        pub = item.get("public_key")
        if name and pub:
            storage.add_contact(name, pub.encode(), None)
