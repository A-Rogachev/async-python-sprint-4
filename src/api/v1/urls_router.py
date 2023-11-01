from typing import Any, Optional

from fastapi import APIRouter, Depends, HTTPException, Response, Request
from fastapi import status as fs_status
from passlib.hash import sha256_crypt
from sqlalchemy.ext.asyncio import AsyncSession

from db.db import get_session
from schemas import short_url as short_url_schema
from services.short_url import short_url_crud

urls_router = APIRouter()


@urls_router.get(
    '/{short_url_id}/',
    response_model=dict[str, Any],
)
async def get_original_url(
    request: Request,
    short_url_id: int,
    db: AsyncSession = Depends(get_session),
    status: Optional[str] = None,
) -> Any:
    """
    Вернуть оригинальный URL.
    """
    obj_from_db = await short_url_crud.get_by_id(
        db=db,
        short_url_id=short_url_id,
    )
    if not obj_from_db:
        raise HTTPException(
            status_code=fs_status.HTTP_404_NOT_FOUND,
            detail='Item not found',
        )
    else:
        if status == 'full_info':
            return short_url_schema.FullInfoUrl(
                **obj_from_db.__dict__
            ).model_dump()
        else:
            await short_url_crud.update_clicks_and_info(
                db=db,
                obj_from_db=obj_from_db,
                client_ip=request.client.host,
            )
            return short_url_schema.OriginalUrl(
                **obj_from_db.__dict__
            ).model_dump()


@urls_router.post(
    '/',
    response_model=short_url_schema.ShortUrlInDB,
    status_code=fs_status.HTTP_201_CREATED,
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

    existing_record = await short_url_crud.get_by_name(
        db=db, short_url_name=short_url_in.shorten_url
    )
    if existing_record:
        raise HTTPException(
            status_code=400,
            detail='Record with the same name already exists'
        )

    new_record = await short_url_crud.create(db=db, obj_in=short_url_in)
    return new_record


@urls_router.delete(
    '/',
    status_code=fs_status.HTTP_410_GONE,
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
            status_code=fs_status.HTTP_404_NOT_FOUND,
            detail='Item not found',
        )
    else:
        await short_url_crud.delete(
            db=db,
            obj_from_db=obj_from_db,
            obj_del_schema=short_url_del,
        )
        return Response(status_code=fs_status.HTTP_204_NO_CONTENT)
