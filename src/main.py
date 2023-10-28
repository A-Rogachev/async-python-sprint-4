from core.config import app_settings
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from api.v1 import base


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