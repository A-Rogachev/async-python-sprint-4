from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from passlib.hash import sha256_crypt
from pydantic import BaseModel
from sqlalchemy import select
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


class ShortUrlRepositoryDB(Repository, Generic[ModelType, CreateSchemaType, DeleteSchemaType]):
    """
    Репозиторий для работы с моделью ShortUrl.
    """
    def __init__(self, model: Type[ModelType]):
        self._model = model

    async def get_by_short_url(self, db: AsyncSession, short_url: str) -> Optional[ModelType]:
        """
        Получение оригинального URL по его короткому URL.
        """
        statement = select(self._model).where(self._model.shorten_url == short_url)
        results = await db.execute(statement=statement)
        return results.scalar_one_or_none()

    async def create(self, db: AsyncSession, *, obj_in: CreateSchemaType) -> ModelType:
        """
        Создание новой записи.
        """
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self._model(**obj_in_data)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def delete(self, db: AsyncSession, *, obj_del: DeleteSchemaType) -> ModelType:
        """
        Удаление записи.
        Для удаления записи требуется кодовое слово, записанное при создании.
        """

        db_obj = await self.get_by_short_url(db=db, short_url=obj_del.shorten_url)
        if sha256_crypt.verify(delete_code, db_obj.delete_code):
            # Delete the record from the database
            db.delete(db_obj)
            await db.commit()

            return db_obj
        else:
            return None
