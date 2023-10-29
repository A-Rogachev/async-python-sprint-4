from typing import Optional
from datetime import datetime

from pydantic import BaseModel


class ShortUrlBase(BaseModel):
    pass

class ShortUrlCreate(ShortUrlBase):
    original_url: str
    shorten_url: str
    password_for_deleting: str

class ShortUrlUpdate(ShortUrlBase):
    pass


class ShortUrlInDBBase(ShortUrlBase):
    id: int
    original_url: str
    shorten_url: str
    created_at: datetime
    deleted_at: Optional[datetime]
    clicks: int

    class Config:
        from_attributes = True


class OriginalUrl(ShortUrlBase):
    original_url: str

class ShortUrlInDB(ShortUrlInDBBase):
    pass
