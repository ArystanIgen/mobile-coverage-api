from typing import Any

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import SiteModel
from app.repository import SiteRepository
from app.schemas.geo_coordinates import GeoPoint
from app.schemas.site import SiteCoverageRow, SiteCreate
from app.tests.factories import create_provider_factory, create_site_factory


@pytest.mark.asyncio
async def test_create_site_model(
    async_session: AsyncSession,
    mock_site_data: dict[str, Any],
):
    created_provider = await create_provider_factory()

    site_repo = SiteRepository()

    site_in = SiteCreate(
        provider_id=created_provider.id,
        **mock_site_data,
    )

    created_site: SiteModel = await site_repo.create(
        async_session,
        obj_in=site_in,
    )

    assert created_site.id is not None
    assert created_site.provider_id == created_provider.id
    assert created_site.longitude == mock_site_data["longitude"]
    assert created_site.latitude == mock_site_data["latitude"]


@pytest.mark.asyncio
async def test_return_nearby_sites_by_specified_longitude_and_latitude(
    async_session: AsyncSession,
    mock_list_of_nearby_geo_coordinates: list[GeoPoint],
):
    provider_in_radius = await create_provider_factory()

    inside_radius_site_coordinates = mock_list_of_nearby_geo_coordinates[0]

    await create_site_factory(
        provider=provider_in_radius,
        longitude=inside_radius_site_coordinates.longitude,
        latitude=inside_radius_site_coordinates.latitude,
        has_2g=True,
        has_3g=False,
        has_4g=True,
    )

    provider_outside_radius = await create_provider_factory()

    outside_radius_site_coordinates = mock_list_of_nearby_geo_coordinates[1]

    await create_site_factory(
        provider=provider_outside_radius,
        longitude=outside_radius_site_coordinates.longitude,
        latitude=outside_radius_site_coordinates.latitude,
        has_2g=False,
        has_3g=True,
        has_4g=False,
    )

    site_repo = SiteRepository()

    nearby_sites: list[SiteCoverageRow] = await site_repo.get_nearby_sites(
        async_session=async_session,
        longitude=inside_radius_site_coordinates.longitude,
        latitude=inside_radius_site_coordinates.latitude,
    )

    assert len(nearby_sites) == 1
    site_coverage = nearby_sites[0]
    assert site_coverage.provider == provider_in_radius.name
    assert site_coverage.g2 is True
    assert site_coverage.g3 is False
    assert site_coverage.g4 is True
