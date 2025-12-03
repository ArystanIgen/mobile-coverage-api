from functools import wraps

import httpx
from loguru import logger

from app.exceptions import BadGatewayError


def raise_if_error(request_func):
    @wraps(request_func)
    async def _(*args, **kwargs):
        try:
            return await request_func(*args, **kwargs)
        except httpx.HTTPError as exc:
            logger.error(f"Adresse API request failed: {exc}")
            raise BadGatewayError() from exc

    return _
