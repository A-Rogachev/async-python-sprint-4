from typing import Any, List

from fastapi import APIRouter


urls_router = APIRouter()


@urls_router.get("/{shorten_url_id}")
async def get_original_url(shorten_url_id: str):
    return {
        "shorten_url_id": shorten_url_id
    }
