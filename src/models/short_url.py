from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, JSON, UUID, String
from .base import Base


ORIGINAL_URL_MAX_LENGTH: int = 50
SHORTEN_URL_MAX_LENGTH: int = 50
PASSWORD_FOR_DELETING_MAX_LENGTH: int = 50


from sqlalchemy.dialects.postgresql import UUID
import uuid


class ShortUrl(Base):
    __tablename__ = 'short_urls'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    original_url = Column(
        String(ORIGINAL_URL_MAX_LENGTH),
        nullable=False,
    )
    shorten_url = Column(
        String(SHORTEN_URL_MAX_LENGTH),
        nullable=False,
        unique=True,
    )
    created_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
    )
    deleted_at = Column(
        DateTime,
        nullable=True,
        default=None,
    )
    total_clicks = Column(
        Integer,
        nullable=False,
        default=0,
    )
    full_info = Column(
        JSON,
        nullable=True,
    )
    password_for_deleting = Column(
        String(PASSWORD_FOR_DELETING_MAX_LENGTH),
        nullable=False,
    )
