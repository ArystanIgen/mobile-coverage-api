from typing import Any

import pytest
import respx
from httpx import AsyncClient, Response

from app.core.config import CONFIG
from app.schemas.geo_coordinates import GeoPoint
from app.tests.factories import create_provider_factory, create_site_factory


@pytest.mark.asyncio
async def test_get_network_coverage_api_returns_availability_map(
    async_client: AsyncClient,
    mock_address: str,
    mock_adresse_api_response: dict[str, Any],
    mock_list_of_nearby_geo_coordinates: list[GeoPoint],
):
    target_coordinates = mock_list_of_nearby_geo_coordinates[0]

    expected_result = {
        "orange": {"2G": True, "3G": False, "4G": False},
        "sfr": {"2G": False, "3G": False, "4G": True},
    }

    for provider_name, sites in expected_result.items():
        created_provider_obj = await create_provider_factory(
            name=provider_name,
        )
        await create_site_factory(
            provider=created_provider_obj,
            longitude=target_coordinates.longitude,
            latitude=target_coordinates.latitude,
            has_2g=sites["2G"],
            has_3g=sites["3G"],
            has_4g=sites["4G"],
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
    assert response.json() == expected_result


@pytest.mark.asyncio
async def test_get_network_coverage_api_returns_not_found(
    async_client: AsyncClient,
):
    unknown_address = "123 Fake Street, London, UK"
    async with respx.mock:
        respx.get(
            CONFIG.adresse_api_url,
            params={"q": unknown_address, "limit": 1},
        ).mock(
            return_value=Response(
                status_code=200,
                json={"features": []},
            )
        )
        response = await async_client.get(
            f"{CONFIG.api.prefix}/v1/network-coverage",
            params={"address": unknown_address},
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
