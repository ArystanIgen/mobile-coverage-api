from typing import Annotated, AsyncGenerator

from fastapi import Depends
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import async_session_factory


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        try:
            yield session
        except Exception as e:
            logger.exception(
                "Session rollback because of exception: {}", e
            )
            await session.rollback()
            raise
        finally:
            await session.close()


AsyncSessionDep = Annotated[AsyncSession, Depends(get_async_session)]
