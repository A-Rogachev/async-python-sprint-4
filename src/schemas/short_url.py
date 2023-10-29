from typing import Optional
from datetime import datetime

from pydantic import BaseModel


class ShortUrlBase(BaseModel):
    title: str

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
        orm_mode = True


class ShortUrl(ShortUrlInDBBase):
    pass

class ShortUrlInDB(ShortUrlInDBBase):
    pass
