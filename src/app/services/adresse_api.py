import httpx
from fastapi import HTTPException
from app.core.config import CONFIG
from app.schemas.address import GeoCoordinates


async def fetch_coordinates_from_address(address: str) -> GeoCoordinates:
    params = {"q": address, "limit": 1}
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
        raise HTTPException(
            status_code=404,
            detail="Address not found",
        )

    longitude, latitude = features[0]["geometry"]["coordinates"]
    return GeoCoordinates(
        longitude=longitude,
        latitude=latitude,
    )
