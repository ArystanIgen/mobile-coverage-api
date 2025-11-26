import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import SiteModel
from app.repository import SiteRepository
from app.schemas.address import GeoCoordinates
from app.schemas.site import SiteCreate
from app.tests.factories import ProviderFactory, SiteFactory


@pytest.mark.asyncio
async def test_create_site_model(
    async_session: AsyncSession,
    mock_site_data: dict[str, str]
):
    created_provider = await ProviderFactory()

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
    mock_list_of_nearby_geo_coordinates: list[GeoCoordinates]
):
    for coordinates in mock_list_of_nearby_geo_coordinates:
        test_provider = await ProviderFactory()
        await SiteFactory(
            provider=test_provider,
            longitude=coordinates.longitude,
            latitude=coordinates.latitude,
        )

    site_repo = SiteRepository()

    nearby_sites: list[SiteModel] = await site_repo.get_nearby_sites(
        async_session=async_session,
        longitude=mock_list_of_nearby_geo_coordinates[0].longitude,
        latitude=mock_list_of_nearby_geo_coordinates[0].latitude,
    )

    assert len(nearby_sites) == 1
    assert nearby_sites[0].longitude == mock_list_of_nearby_geo_coordinates[0].longitude
    assert nearby_sites[0].latitude == mock_list_of_nearby_geo_coordinates[0].latitude
