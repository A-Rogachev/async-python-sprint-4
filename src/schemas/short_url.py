from typing import Optional
from datetime import datetime

from pydantic import BaseModel


class ShortUrlBase(BaseModel):
    pass

class ShortUrlCreate(ShortUrlBase):
    pass

class ShortUrlUpdate(ShortUrlBase):
    pass


class ShortUrlInDBBase(ShortUrlBase):
    original_url: str
    shorten_url_id: str
    created_at: datetime
    deleted_at: Optional[datetime]
    clicks: int

    class Config:
        from_attributes = True


class OriginalUrl(ShortUrlBase):
    original_url: str

class ShortUrlInDB(ShortUrlInDBBase):
    pass
