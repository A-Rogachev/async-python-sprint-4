from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status, Response
from passlib.hash import sha256_crypt
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
    obj_from_db = await short_url_crud.get_by_short_url(db=db, short_url=short_url)
    if not obj_from_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Item not found',
        )
    return obj_from_db


@urls_router.post(
    '/',
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
    encrypted_password = sha256_crypt.hash(short_url_in.password_for_deleting)
    short_url_in.password_for_deleting = encrypted_password
    new_record = await short_url_crud.create(db=db, obj_in=short_url_in)
    return new_record


@urls_router.delete(
    '/',
    status_code=status.HTTP_410_GONE,
)
async def delete_shorten_url(
    *,
    db: AsyncSession = Depends(get_session),
    short_url_del: short_url_schema.ShortUrlDelete,
) -> Any:
    """
    Удаление существующей записи.
    """
    obj_from_db = await short_url_crud.get_by_short_url(
        db=db,
        short_url=short_url_del.shorten_url,
    )
    if not obj_from_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Item not found',
        )
    else:
        await short_url_crud.delete(
            db=db,
            obj_from_db=obj_from_db,
            obj_del_schema=short_url_del,
        )
        return Response(status_code=status.HTTP_204_NO_CONTENT)
