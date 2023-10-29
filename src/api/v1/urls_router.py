from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from db.db import get_session
from schemas import short_url as short_url_schema
from services.short_url import short_url_crud

urls_router = APIRouter()


@urls_router.get('/{short_url}', response_model=short_url_schema.OriginalUrl)
async def get_original_url(
    *,
    db: AsyncSession = Depends(get_session),
    short_url: str
) -> Any:
    """
    Вернуть оригинальный URL.
    """
    original_url: str = await short_url_crud.get_by_short_url(db=db, short_url=short_url)
    if not original_url:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Item not found',
        )
    return original_url


@urls_router.post(
    "/",
    response_model=short_url_schema.ShortUrlInDB,
    status_code=status.HTTP_201_CREATED,
)
async def create_shorten_url(
    *,
    db: AsyncSession = Depends(get_session),
    short_url_in: short_url_schema.ShortUrlCreate,
) -> Any:
    """
    Создание новой записи сокращенной ссылки.
    """
    new_record = await short_url_crud.create(db=db, obj_in=short_url_in)
    return new_record
