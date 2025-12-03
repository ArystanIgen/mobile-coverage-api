from typing import Any, Never

import pytest
import respx
from httpx import Response

from app.core.config import CONFIG
from app.exceptions import AddressNotFoundError
from app.services.adresse_api import fetch_coordinates_from_address


@pytest.mark.asyncio
async def test_fetch_coordinates_success(
    mock_adresse_api_response: dict[str, Any],
    mock_address: str,
):
    async with respx.mock:
        respx.get(CONFIG.adresse_api_url).mock(
            return_value=Response(
                status_code=200,
                json=mock_adresse_api_response,
            )
        )

        coordinates = await fetch_coordinates_from_address(mock_address)

        expected_longitude, expected_latitude = mock_adresse_api_response[
            "features"
        ][0]["geometry"]["coordinates"]

        assert coordinates.longitude == expected_longitude
        assert coordinates.latitude == expected_latitude


@pytest.mark.asyncio
async def test_fetch_coordinates_not_found():
    mock_response_data: dict[str, list[Never]] = {"features": []}

    async with respx.mock:
        respx.get(CONFIG.adresse_api_url).mock(
            return_value=Response(
                status_code=200,
                json=mock_response_data,
            )
        )

        with pytest.raises(AddressNotFoundError) as exc_info:
            await fetch_coordinates_from_address("Unknown Place")

        assert exc_info.value.status_code == 404
        assert exc_info.value.message == "Address not found"
