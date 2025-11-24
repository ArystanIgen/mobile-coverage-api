from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI
from loguru import logger

from app.core.config import CONFIG
from app.services.data_ingestion import seed_providers_and_sites
from app.api.v1.api import api_router
from app.api.v1.endpoints.health import router as health_router

from starlette.middleware.cors import CORSMiddleware


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

main_app.add_middleware(
    CORSMiddleware,
    allow_origins=CONFIG.api.allowed_hosts or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

main_app.include_router(router=api_router, prefix=CONFIG.api.prefix)
main_app.include_router(
    router=health_router,
    prefix=f"{CONFIG.api.prefix}/health",
    tags=["API Health"],
)
