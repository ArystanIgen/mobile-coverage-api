from fastapi import APIRouter, Query, status

from app.api.deps.repos import SiteRepoDep
from app.api.deps.session import (
    AsyncSessionDep,
)
from app.exceptions import AddressNotFoundError, BadGatewayError
from app.exceptions.openapi_handler import openapi_handle_error
from app.schemas.geo_coordinates import GeoPoint
from app.schemas.network_coverage import (
    NetworkAvailability,
    OperatorsAvailability,
)
from app.schemas.site import SiteCoverageRow
from app.services.adresse_api import fetch_coordinates_from_address

router = APIRouter()


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=OperatorsAvailability,
    responses=openapi_handle_error(
        AddressNotFoundError,
        BadGatewayError
    ),
    summary="Lookup mobile coverage for an address",
    description="Returns 2G/3G/4G availability by "
                "operator for the address provided. ",
    operation_id="lookupNetworkCoverage",
    response_description="Coverage map keyed by operator name",
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

    fetched_nearby_sites: list[
        SiteCoverageRow
    ] = await site_repo.get_nearby_sites(
        async_session=async_session,
        longitude=geo_coordinates.longitude,
        latitude=geo_coordinates.latitude,
    )

    network_coverages: OperatorsAvailability = {}

    for site_coverage in fetched_nearby_sites:
        network_coverages[site_coverage.provider] = NetworkAvailability(
            g2=site_coverage.g2,
            g3=site_coverage.g3,
            g4=site_coverage.g4,
        )

    return network_coverages
