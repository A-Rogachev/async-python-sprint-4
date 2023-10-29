from datetime import datetime
from sqlalchemy import Column, String, DateTime, Integer

from .base import Base


class ShortUrl(Base):
    __tablename__ = 'short_urls'

    id = Column(Integer, primary_key=True)
    original_url = Column(String, nullable=False)
    shorten_url = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True, default=None)
    clicks = Column(Integer, nullable=False, default=0)
    password_for_deleting = Column(String, nullable=False)