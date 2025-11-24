from fastapi import APIRouter

from app.api.v1.endpoints.network_coverage import (
    router as network_coverage_router,
)

api_router = APIRouter()

api_router.include_router(
    prefix="/v1/network-coverage",
    router=network_coverage_router,
    tags=["network-coverage"],
)
