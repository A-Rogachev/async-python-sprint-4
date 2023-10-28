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


# 2. Создание и запись урлов - модель в БД плюс миграции Алембик
# 3. Возможность удаления сохраненного урл (только для автора)
# 4. middleware блокирует доступ из запрещенных подсетей.




if __name__ == '__main__':
    from sqlalchemy.ext.asyncio import create_async_engine
    from sqlalchemy.orm import declarative_base

    Base = declarative_base()

    engine = create_async_engine(app_settings.database_dsn, echo=True)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
        reload=True,
        # log_config=LOGGING,
    )

