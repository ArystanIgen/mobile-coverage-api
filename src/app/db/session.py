from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import CONFIG

async_engine = create_async_engine(
    url=CONFIG.db.async_url,
    pool_size=CONFIG.db.pool_size,
    max_overflow=CONFIG.db.max_overflow,
    echo=CONFIG.db.echo,
    future=CONFIG.db.future,
)

async_session_factory = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)
