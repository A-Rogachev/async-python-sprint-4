from core.config import app_settings
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from api.v1 import base
import uvicorn
from core.logger import LOGGING


app = FastAPI(
    title=app_settings.app_title,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
) 
app.include_router(base.api_router, prefix="/api/v1") 


# 1. Доступность бд
# 2. клики по переходу на урл
# 3. Возможность удаления сохраненного урл (только для автора)
# 4. middleware блокирует доступ из запрещенных подсетей.




if __name__ == '__main__':

    # # Создание таблиц вручную
    # from sqlalchemy.ext.asyncio import create_async_engine
    # from sqlalchemy.orm import declarative_base
    # import asyncio
    # from models.short_url import ShortUrl
    # from sqlalchemy.util import immutabledict

    # Base = declarative_base()
    # tables = immutabledict({'short_urls': ShortUrl.__table__})
    # Base.metadata.tables = tables
    # engine = create_async_engine(str(app_settings.database_dsn), echo=True)
    # async def init_models():
    #     async with engine.begin() as conn:
    #         await conn.run_sync(Base.metadata.drop_all)
    #         await conn.run_sync(Base.metadata.create_all)
    # asyncio.run(init_models())

    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
        reload=True,
        # log_config=LOGGING,
    )

