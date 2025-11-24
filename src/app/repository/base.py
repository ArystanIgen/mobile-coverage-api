from typing import Generic, List, Optional, Type, TypeVar

from loguru import logger
from pydantic import BaseModel
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import BaseModel as DBBaseModel

ModelType = TypeVar("ModelType", bound=DBBaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    CRUD object with default methods to Create, Read, Update, Delete (CRUD).
    * `model`: A SQLAlchemy model class
    """

    model: Type[ModelType]

    async def get_multi(
        self, async_session: AsyncSession, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        stmt = (
            select(self.model)
            .order_by(self.model.id)
            .offset(skip)
            .limit(limit)
        )
        query = await async_session.execute(stmt)
        return query.scalars().all()

    async def create(
        self, async_session: AsyncSession, *, obj_in: CreateSchemaType
    ) -> Optional[ModelType]:  # noqa
        try:
            obj_in_data = obj_in.model_dump(mode="python", exclude_none=True)
            db_obj = self.model(**obj_in_data)
            async_session.add(db_obj)
            await async_session.commit()
            await async_session.refresh(db_obj)
            return db_obj
        except Exception as e:
            logger.error(e)
            await async_session.rollback()
            raise

    async def create_bulk(
        self, async_session: AsyncSession, *, objs_in: List[CreateSchemaType]
    ) -> List[ModelType]:
        try:
            objs_data = [
                obj.model_dump(mode="python", exclude_none=True)
                for obj in objs_in
            ]

            db_objs = [self.model(**data) for data in objs_data]

            async_session.add_all(db_objs)
            await async_session.commit()

            for obj in db_objs:
                await async_session.refresh(obj)

            return db_objs

        except Exception as e:
            logger.error(e)
            await async_session.rollback()
            raise

    async def update(
        self,
        async_session: AsyncSession,
        *,
        instance: ModelType,
        obj_update: UpdateSchemaType,
    ) -> Optional[ModelType]:
        update_data = obj_update.model_dump(
            mode="python", exclude_unset=True, exclude_none=True
        )
        for key, value in update_data.items():
            setattr(instance, key, value)
        await async_session.commit()
        await async_session.refresh(instance)
        return instance

    async def remove(
        self, async_session: AsyncSession, *, id_: int
    ) -> Optional[ModelType]:
        query = delete(self.model).where(self.model.id == id_)
        await async_session.execute(query)
        await async_session.commit()
        return None
