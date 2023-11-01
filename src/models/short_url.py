from datetime import datetime
from sqlalchemy import Column, String, DateTime, Integer, JSON

from .base import Base


class ShortUrl(Base):
    __tablename__ = 'short_urls'

    id = Column(Integer, primary_key=True)
    original_url = Column(String, nullable=False)
    shorten_url = Column(String, nullable=False, unique=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True, default=None)
    total_clicks = Column(Integer, nullable=False, default=0)
    full_info = Column(JSON, nullable=True)
    password_for_deleting = Column(String, nullable=False)
