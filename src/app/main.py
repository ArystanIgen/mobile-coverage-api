from fastapi import FastAPI

from app.core.config import CONFIG

main_app = FastAPI(
    title=CONFIG.api.title,
    debug=CONFIG.api.debug,
    version=CONFIG.api.version,
    openapi_url=f"{CONFIG.api.prefix}/openapi.json",
    docs_url=f"{CONFIG.api.prefix}/docs",
    redoc_url=f"{CONFIG.api.prefix}/redoc",
)
