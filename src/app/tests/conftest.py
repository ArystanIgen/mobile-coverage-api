import asyncio
from asyncio import AbstractEventLoop
from typing import AsyncGenerator, Generator

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy_utils import create_database, database_exists, drop_database

from app.api.deps.session import get_async_session
from app.core.config import CONFIG
from app.db.session import async_engine as test_async_engine
from app.main import main_app
from app.models import BaseModel
from app.tests.factories import ProviderFactory, SiteFactory
from app.tests.fixtures import *  # noqa


@pytest.fixture
def event_loop(request) -> Generator[AbstractEventLoop, None, None]:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def test_engine():
    if not database_exists(CONFIG.db.url):
        create_database(CONFIG.db.url)

    async with test_async_engine.begin() as conn:
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS postgis"))
        await conn.run_sync(BaseModel.metadata.create_all)

    yield test_async_engine

    async with test_async_engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.drop_all)

    await test_async_engine.dispose()
    drop_database(CONFIG.db.url)


@pytest_asyncio.fixture
async def async_session(test_engine) -> AsyncGenerator[AsyncSession, None]:
    async_session_factory = async_sessionmaker(
        test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    async with async_session_factory() as session:
        try:
            await session.begin()
            ProviderFactory._meta.sqlalchemy_session = session  # type: ignore[attr-defined]
            SiteFactory._meta.sqlalchemy_session = session  # type: ignore[attr-defined]
            yield session
        finally:
            await session.rollback()


@pytest_asyncio.fixture
async def async_client(async_session: AsyncSession):
    def _get_db_override():
        return async_session  # pragma: no cover

    main_app.dependency_overrides[get_async_session] = _get_db_override

    transport = ASGITransport(app=main_app)
    async with AsyncClient(
        transport=transport,
        base_url=CONFIG.api.host,
    ) as client:
        yield client

    main_app.dependency_overrides.clear()
