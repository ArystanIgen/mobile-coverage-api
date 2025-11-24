from app.db.session import async_session_factory

from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import Depends

from typing import Annotated, AsyncGenerator

from loguru import logger


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        try:
            yield session
        except Exception as e:
            logger.exception(
                "Session rollback because of exception: {}", e
            )
            await session.rollback()
        finally:
            await session.close()


AsyncSessionDep = Annotated[AsyncSession, Depends(get_async_session)]
