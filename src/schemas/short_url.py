from typing import Optional
from datetime import datetime

from pydantic import BaseModel


class ShortUrlBase(BaseModel):
    pass

class ShortUrlCreate(ShortUrlBase):
    """
    Схема, используемая при создании нового сокращенного URL.
    """
    original_url: str
    shorten_url: str
    password_for_deleting: str

class ShortUrlDelete(ShortUrlBase):
    """
    Схема, используемая при удалении сокращенного URL.
    """
    shorten_url: str
    password_for_deleting: str


class ShortUrlInDB(ShortUrlBase):
    id: int
    original_url: str
    shorten_url: str
    created_at: datetime

    class Config:
        from_attributes = True


class OriginalUrl(ShortUrlBase):
    original_url: str
