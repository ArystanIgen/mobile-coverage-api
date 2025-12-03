from typing import Mapping

import httpx
from loguru import logger

from app.core.config import CONFIG
from app.exceptions import AddressNotFoundError
from app.schemas.geo_coordinates import GeoPoint
from app.services.helper import raise_if_error

transport = httpx.AsyncHTTPTransport(
    retries=3,
)


@raise_if_error
async def fetch_coordinates_from_address(address: str) -> GeoPoint:
    params: Mapping[str, str | int] = {"q": address, "limit": 1}

    async with httpx.AsyncClient(
        transport=transport,
        timeout=5.0,
    ) as client:
        resp = await client.get(
            url=CONFIG.adresse_api_url,
            params=params,
        )
        resp.raise_for_status()
        data = resp.json()

    features = data.get("features") or []
    if not features:
        logger.warning(f"Address not found: {address}")
        raise AddressNotFoundError()

    longitude, latitude = features[0]["geometry"]["coordinates"]
    return GeoPoint(
        longitude=longitude,
        latitude=latitude,
    )
