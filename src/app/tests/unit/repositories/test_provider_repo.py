import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import ProviderModel
from app.repository import ProviderRepository
from app.schemas.provider import ProviderCreate
from app.tests.factories import ProviderFactory


@pytest.mark.asyncio
async def test_create_provider_model(
    async_session: AsyncSession,
    mock_provider_data: dict[str, str]
):
    provider_repo = ProviderRepository()

    provider_in = ProviderCreate(**mock_provider_data)

    created_provider: ProviderModel = await provider_repo.create(
        async_session,
        obj_in=provider_in,
    )

    assert created_provider.id is not None
    assert created_provider.name == mock_provider_data["name"]
    assert created_provider.mobile_network_code == mock_provider_data[
        'mobile_network_code'
    ]


@pytest.mark.asyncio
async def test_return_provider_by_mobile_network_code(
    async_session: AsyncSession,
):
    provider_repo = ProviderRepository()

    created_provider = await ProviderFactory()

    fetched_provider: ProviderModel = await provider_repo.get_provider_by_mobile_network_code(
        async_session=async_session,
        mobile_network_code=created_provider.mobile_network_code,
    )

    assert fetched_provider.id is not None
    assert fetched_provider.name == created_provider.name
    assert fetched_provider.mobile_network_code == created_provider.mobile_network_code
