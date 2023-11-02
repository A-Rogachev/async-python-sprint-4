from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class ShortUrlBase(BaseModel):
    """
    Базовая модель для URL.
    """
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
    """
    Возвращает отображение модели при создании URL.
    """

    id: UUID
    original_url: str
    shorten_url: str
    created_at: datetime

    class Config:
        from_attributes = True


class OriginalUrl(ShortUrlBase):
    """
    Для вывода оригинального URL.
    """

    original_url: str


class FullInfoUrl(ShortUrlBase):
    """
    Для вывода полной информации о URL.
    """

    id: UUID
    original_url: str
    shorten_url: str
    total_clicks: int
    full_info: dict
