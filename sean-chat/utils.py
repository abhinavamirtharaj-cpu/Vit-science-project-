"""Utility helpers for SEAN CLI"""
from datetime import datetime
import base64
import hashlib
import uuid
from typing import Union


def now_ts() -> str:
    """Return current timestamp formatted YYYY-MM-DD HH:MM"""
    return datetime.now().strftime("%Y-%m-%d %H:%M")


def ts_for_db() -> str:
    return datetime.now().isoformat()


def human_size(n_bytes: int) -> str:
    """Human readable size (KB with 1 decimal)"""
    if n_bytes < 1024:
        return f"{n_bytes}B"
    kb = n_bytes / 1024
    if kb < 1024:
        return f"{kb:.1f}KB"
    mb = kb / 1024
    return f"{mb:.2f}MB"


def sanitize_name(name: str) -> str:
    return name.strip()


def gen_packet_id() -> str:
    return uuid.uuid4().hex


def sha256_hex(data: Union[bytes, str]) -> str:
    if isinstance(data, str):
        data = data.encode()
    return hashlib.sha256(data).hexdigest()


def b64enc(data: bytes) -> str:
    return base64.b64encode(data).decode()


def b64dec(text: str) -> bytes:
    return base64.b64decode(text)
