from .urls_router import urls_router
from .db_router import db_router
from fastapi import APIRouter


api_router = APIRouter()
api_router.include_router(urls_router, prefix='/urls', tags=['urls'])
api_router.include_router(db_router, prefix='/db', tags=['db'])