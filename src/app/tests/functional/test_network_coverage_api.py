from typing import Any

import pytest
import respx
from httpx import AsyncClient, Response

from app.core.config import CONFIG
from app.models import ProviderModel
from app.schemas.geo_coordinates import GeoPoint
from app.tests.factories import create_provider_factory, create_site_factory


@pytest.mark.asyncio
async def test_get_network_coverage_api_returns_availability_map(
    async_client: AsyncClient,
    mock_address: str,
    mock_adresse_api_response: dict[str, Any],
):
    target_coordinates = GeoPoint(latitude=48.8566, longitude=2.3522)

    orange_provider: ProviderModel = await create_provider_factory(
        name="orange",
    )
    sfr_provider: ProviderModel = await create_provider_factory(
        name="sfr",
    )

    await create_site_factory(
        provider=orange_provider,
        longitude=target_coordinates.longitude,
        latitude=target_coordinates.latitude,
        has_2g=True,
        has_3g=False,
        has_4g=False,
    )

    await create_site_factory(
        provider=sfr_provider,
        longitude=target_coordinates.longitude,
        latitude=target_coordinates.latitude,
        has_2g=False,
        has_3g=False,
        has_4g=True,
    )

    async with respx.mock:
        respx.get(
            CONFIG.adresse_api_url,
            params={"q": mock_address, "limit": 1},
        ).mock(
            return_value=Response(
                status_code=200,
                json=mock_adresse_api_response,
            )
        )
        response = await async_client.get(
            f"{CONFIG.api.prefix}/v1/network-coverage",
            params={"address": mock_address},
        )

    assert response.status_code == 200
    assert response.json() == {
        "orange": {"2G": False, "3G": False, "4G": False},
        "sfr": {"2G": False, "3G": False, "4G": False},
        "free": {"2G": False, "3G": False, "4G": False},
        "bouygues": {"2G": False, "3G": False, "4G": False},
    }


@pytest.mark.asyncio
async def test_get_network_coverage_api_returns_not_found(
    async_client: AsyncClient,
    mock_address: str,
):
    async with respx.mock:
        respx.get(
            CONFIG.adresse_api_url,
            params={"q": mock_address, "limit": 1},
        ).mock(
            return_value=Response(
                status_code=200,
                json={"features": []},
            )
        )
        response = await async_client.get(
            f"{CONFIG.api.prefix}/v1/network-coverage",
            params={"address": mock_address},
        )

    assert response.status_code == 404

    response_json = response.json()
    assert response_json["detail"] == "Address not found"


@pytest.mark.asyncio
async def test_get_network_coverage_api_fails_with_invalid_address(
    async_client: AsyncClient,
):
    response = await async_client.get(
        f"{CONFIG.api.prefix}/v1/network-coverage",
        params={"address": "a"},
    )

    assert response.status_code == 400

    response_json = response.json()
    assert response_json["code"] == "InvalidRequest"
