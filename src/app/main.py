import sys

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from loguru import logger
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware

from app.api.v1.api import api_router
from app.api.v1.endpoints.health import router as health_router
from app.core.config import CONFIG
from app.core.middlewares import (
    add_process_time_header,
    api_error_handler,
    log_requests,
    validation_exception_handler,
)
from app.exceptions import APIError

logger.remove()


def safe_format(record):
    record["extra"].setdefault("request_id", "N/A")
    record["extra"].setdefault("span_id", "N/A")
    record["extra"].setdefault("trace_id", "N/A")


logger.configure(patcher=safe_format)
logger.add(
    sys.stderr,
    colorize=True,
    enqueue=True,
    format=CONFIG.logger_custom_formatter,
    backtrace=True,
    diagnose=True,
    level="INFO",
    serialize=False,
    catch=True,
)

main_app = FastAPI(
    title=CONFIG.api.title,
    debug=CONFIG.api.debug,
    version=CONFIG.api.version,
    openapi_url=f"{CONFIG.api.prefix}/openapi.json",
    docs_url=f"{CONFIG.api.prefix}/docs",
    redoc_url=f"{CONFIG.api.prefix}/redoc",
)

main_app.add_middleware(
    CORSMiddleware,
    allow_origins=CONFIG.api.allowed_hosts or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
main_app.add_middleware(BaseHTTPMiddleware, dispatch=add_process_time_header)
main_app.add_middleware(BaseHTTPMiddleware, dispatch=log_requests)

main_app.add_exception_handler(
    RequestValidationError,
    validation_exception_handler,  # type:ignore
)
main_app.add_exception_handler(APIError, api_error_handler)  # type:ignore

main_app.include_router(router=api_router, prefix=CONFIG.api.prefix)
main_app.include_router(
    router=health_router,
    prefix=f"{CONFIG.api.prefix}/health",
    tags=["API Health"],
)
