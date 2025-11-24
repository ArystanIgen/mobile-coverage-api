from fastapi import APIRouter, Query, status

from app.api.deps import (
    AsyncSessionDep,
)
from app.schemas.network_coverage import OperatorsAvailability

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
    address: str = Query(
        ...,
        min_length=3,
        max_length=200,
        description="Textual address, e.g. '42 rue papernest 75011 Paris'"
    ),
) -> OperatorsAvailability:
    response = {
        "orange": {"2G": True, "3G": True, "4G": False},
        "sfr": {"2G": True, "3G": True, "4G": True}
    }
    return OperatorsAvailability(**response)
