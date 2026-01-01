"""
chat_service.py - storage-only wrapper

This file now acts as a small wrapper that re-exports the storage CSV API implemented in `storage.py`.
Use `storage.py` as the canonical implementation for CSV persistence.
"""

from storage import append_message, append_messages, get_history, get_csv_path

__all__ = ["append_message", "append_messages", "get_history", "get_csv_path"]
