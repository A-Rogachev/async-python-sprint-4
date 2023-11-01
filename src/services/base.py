from datetime import datetime
from typing import Generic, Optional, Type, TypeVar

from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from passlib.hash import sha256_crypt
from pydantic import BaseModel
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from models.base import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
DeleteSchemaType = TypeVar('DeleteSchemaType', bound=BaseModel)


class Repository:

    def get(self, *args, **kwargs):
        raise NotImplementedError

    def get_multi(self, *args, **kwargs):
        raise NotImplementedError

    def create(self, *args, **kwargs):
        raise NotImplementedError

    def update(self, *args, **kwargs):
        raise NotImplementedError

    def delete(self, *args, **kwargs):
        raise NotImplementedError


class ShortUrlRepositoryDB(
    Repository,
    Generic[ModelType, CreateSchemaType, DeleteSchemaType],
):
    """
    Репозиторий для работы с моделью ShortUrl.
    """
    def __init__(self, model: Type[ModelType]):
        self._model = model

    async def get_by_id(
        self,
        db: AsyncSession, short_url_id: int,
    ) -> Optional[ModelType]:
        """
        Получение оригинального URL по его короткому URL.
        """
        statement = select(self._model).where(
            self._model.id == short_url_id,
        )
        results = await db.execute(statement=statement)
        obj_in_db = results.scalar_one_or_none()
        if obj_in_db and obj_in_db.deleted_at:
            raise HTTPException(
                status_code=status.HTTP_410_GONE,
                detail='Item has been deleted.',
            )
        return obj_in_db

    async def create(
        self,
        db: AsyncSession,
        *,
        obj_in: CreateSchemaType,
    ) -> ModelType:
        """
        Создание новой записи.
        """
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self._model(**obj_in_data)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def delete(
        self,
        db: AsyncSession,
        obj_from_db: ModelType,
        obj_del_schema: DeleteSchemaType,
    ) -> None:
        """
        Удаление записи.
        Для удаления записи требуется кодовое слово, записанное при создании.
        """
        if sha256_crypt.verify(
            obj_del_schema.password_for_deleting,
            obj_from_db.password_for_deleting,
        ):
            obj_from_db.deleted_at = datetime.now()
            await db.commit()
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='Wrong password for deleting',
            )

    async def update_clicks_and_info(
        self,
        db: AsyncSession,
        obj_from_db: ModelType,
        client_ip: str,
    ) -> None:
        """
        Обновление количества кликов и информации.
        """
        obj_from_db.total_clicks += 1
        if not obj_from_db.full_info:
            obj_from_db.full_info = {}
        full_info = obj_from_db.full_info
        full_info.update(
            {datetime.now().strftime("%Y-%m-%d %H:%M:%S"): client_ip}
        )
        statement = update(self._model).where(
            self._model.id == obj_from_db.id,
        ).values(full_info=full_info)
        await db.execute(statement=statement)
        await db.commit()
