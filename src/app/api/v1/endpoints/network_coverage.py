from fastapi import APIRouter, Query, status

from app.api.deps.repos import SiteRepoDep
from app.api.deps.session import (
    AsyncSessionDep,
)
from app.models import SiteModel
from app.schemas.geo_coordinates import GeoPoint
from app.schemas.network_coverage import (
    NetworkAvailability,
    OperatorsAvailability,
)
from app.services.adresse_api import fetch_coordinates_from_address

router = APIRouter()


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=OperatorsAvailability,
    summary="GetNetworkCoverage",
    description="Get Network Coverage",
    operation_id="GetNetworkCoverage",
    response_description="Network Coverage",
)
async def get_network_coverage_api(
    async_session: AsyncSessionDep,
    site_repo: SiteRepoDep,
    address: str = Query(
        ...,
        min_length=3,
        max_length=200,
        description="Textual address, e.g. '42 rue papernest 75011 Paris'",
    ),
) -> OperatorsAvailability:
    geo_coordinates: GeoPoint = await fetch_coordinates_from_address(
        address=address,
    )

    fetched_nearby_sites: list[SiteModel] = await site_repo.get_nearby_sites(
        async_session=async_session,
        longitude=geo_coordinates.longitude,
        latitude=geo_coordinates.latitude,
    )

    network_coverages: OperatorsAvailability = {
        "orange": NetworkAvailability(g2=False, g3=False, g4=False),
        "sfr": NetworkAvailability(g2=False, g3=False, g4=False),
        "free": NetworkAvailability(g2=False, g3=False, g4=False),
        "bouygues": NetworkAvailability(g2=False, g3=False, g4=False),
    }

    for site in fetched_nearby_sites:
        provider_name = site.provider.name

        if provider_name not in network_coverages:
            continue

        coverage = network_coverages[provider_name]

        coverage.g2 = coverage.g2 or site.has_2g
        coverage.g3 = coverage.g3 or site.has_3g
        coverage.g4 = coverage.g4 or site.has_4g

    return network_coverages
