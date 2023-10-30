from fastapi import APIRouter, Depends
from fastapi.responses import ORJSONResponse
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from db.db import get_session

db_router = APIRouter()


class PingResponse(BaseModel):
    status: str


@db_router.get(
    '/ping',
    responses={
        200: {'model': PingResponse, 'description': 'Database is available'},
        500: {'model': PingResponse, 'description': 'Internal server error'},
    },
)
async def ping(db: AsyncSession = Depends(get_session)):
    """
    Проверка доступности базы данных.
    """
    try:
        await db.execute(text('SELECT 1'))
        return ORJSONResponse(
            content={'status': 'database is available'},
            status_code=200,
        )
    except Exception as error:
        return ORJSONResponse(
            content={'status': f'database is not available: {error}'},
            status_code=500,
        )
