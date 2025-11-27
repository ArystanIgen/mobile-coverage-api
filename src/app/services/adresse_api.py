from typing import Mapping

import httpx
from fastapi import HTTPException
from loguru import logger

from app.core.config import CONFIG
from app.schemas.geo_coordinates import GeoPoint


async def fetch_coordinates_from_address(address: str) -> GeoPoint:
    params: Mapping[str, str | int] = {"q": address, "limit": 1}
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            url=CONFIG.adresse_api_url,
            params=params,
            timeout=5.0,
        )
        resp.raise_for_status()
        data = resp.json()

    features = data.get("features") or []
    if not features:
        logger.warning(f"Address not found: {address}")
        raise HTTPException(
            status_code=404,
            detail="Address not found",
        )

    longitude, latitude = features[0]["geometry"]["coordinates"]
    return GeoPoint(
        longitude=longitude,
        latitude=latitude,
    )
