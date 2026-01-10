"""
database.py
PostgreSQL database support for persistent chat history storage.
Uses environment variable DATABASE_URL for connection.
Falls back to CSV if DATABASE_URL is not set.
"""

import os
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

class ChatMessage(Base):
    __tablename__ = 'chat_messages'
    
    id = Column(Integer, primary_key=True)
    contact_id = Column(String(255), index=True)
    contact_name = Column(String(255))
    direction = Column(String(50))  # 'sent' or 'received'
    iso_time = Column(String(100))
    date = Column(String(50))
    time = Column(String(50))
    text = Column(Text)
    sentiment_polarity = Column(Float)
    sentiment_category = Column(String(100))
    sentiment_emoji = Column(String(50))
    color_hex = Column(String(20))
    saved_at = Column(DateTime, default=datetime.utcnow)

# Global database session
_engine = None
_Session = None

def init_db(database_url=None):
    """Initialize database connection. Call this once at startup."""
    global _engine, _Session
    
    if database_url is None:
        database_url = os.environ.get('DATABASE_URL')
    
    if not database_url:
        return False  # Fall back to CSV
    
    # Render uses postgres:// but SQLAlchemy needs postgresql://
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    
    try:
        _engine = create_engine(database_url, pool_pre_ping=True)
        Base.metadata.create_all(_engine)
        _Session = sessionmaker(bind=_engine)
        return True
    except Exception as e:
        print(f"Database initialization failed: {e}")
        return False

def get_session():
    """Get a new database session."""
    if _Session is None:
        return None
    return _Session()

def is_db_enabled():
    """Check if database is enabled."""
    return _engine is not None

def append_message_db(contact, message):
    """Append a message to PostgreSQL database."""
    session = get_session()
    if not session:
        return False
    
    try:
        msg = ChatMessage(
            contact_id=contact.get('id'),
            contact_name=contact.get('name'),
            direction=message.get('dir'),
            iso_time=message.get('iso', ''),
            date=message.get('date', ''),
            time=message.get('time', ''),
            text=message.get('text', ''),
            sentiment_polarity=float(message.get('sentiment_polarity', 0)) if message.get('sentiment_polarity') else None,
            sentiment_category=message.get('sentiment_category', ''),
            sentiment_emoji=message.get('sentiment_emoji', ''),
            color_hex=message.get('color_hex', ''),
            saved_at=datetime.utcnow()
        )
        session.add(msg)
        session.commit()
        return True
    except Exception as e:
        print(f"Database write failed: {e}")
        session.rollback()
        return False
    finally:
        session.close()

def get_history_db(contact_id):
    """Get message history from PostgreSQL database."""
    session = get_session()
    if not session:
        return []
    
    try:
        messages = session.query(ChatMessage).filter_by(
            contact_id=contact_id
        ).order_by(ChatMessage.saved_at).all()
        
        return [{
            'contact_id': msg.contact_id,
            'contact_name': msg.contact_name,
            'dir': msg.direction,
            'iso': msg.iso_time,
            'date': msg.date,
            'time': msg.time,
            'text': msg.text,
            'sentiment_polarity': msg.sentiment_polarity,
            'sentiment_category': msg.sentiment_category,
            'sentiment_emoji': msg.sentiment_emoji,
            'color_hex': msg.color_hex,
            'saved_at': msg.saved_at.isoformat() if msg.saved_at else ''
        } for msg in messages]
    except Exception as e:
        print(f"Database read failed: {e}")
        return []
    finally:
        session.close()

def get_all_messages_db():
    """Get all messages from database for analysis."""
    session = get_session()
    if not session:
        return []
    
    try:
        messages = session.query(ChatMessage).order_by(ChatMessage.saved_at).all()
        return [{
            'contact_id': msg.contact_id,
            'text': msg.text,
            'sentiment_category': msg.sentiment_category,
            'sentiment_polarity': msg.sentiment_polarity
        } for msg in messages]
    except Exception as e:
        print(f"Database read failed: {e}")
        return []
    finally:
        session.close()
