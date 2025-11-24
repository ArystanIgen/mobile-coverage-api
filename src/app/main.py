from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI
from loguru import logger

from app.core.config import CONFIG
from app.services.data_ingestion import seed_providers_and_sites


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    try:
        await seed_providers_and_sites()
        yield
    except Exception:
        logger.exception("Startup failed during lifespan")
        raise


main_app = FastAPI(
    title=CONFIG.api.title,
    debug=CONFIG.api.debug,
    version=CONFIG.api.version,
    openapi_url=f"{CONFIG.api.prefix}/openapi.json",
    docs_url=f"{CONFIG.api.prefix}/docs",
    redoc_url=f"{CONFIG.api.prefix}/redoc",
    lifespan=lifespan,
)
