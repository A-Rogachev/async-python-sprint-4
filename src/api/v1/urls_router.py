from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from db.db import get_session

urls_router = APIRouter()


@urls_router.get('/{shorten_url_id}')
async def get_original_url(
    *,
    db: AsyncSession = Depends(get_session),
    short_url: str
) -> Any:
    """
    Вернуть оригинальный URL.
    """
    original_url = {}
    if not original_url:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return original_url

# @urls_router.post('/')
# async def create_short_url(db: AsyncSession = Depends(get_session)):
#     return {
#         "url": url
#     }
