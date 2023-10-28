from typing import Any, List

from fastapi import APIRouter


db_router = APIRouter()


@db_router.get("/ping")
async def get_db_accessibility():
    return {
        "works": 'fine'
    }
