from pathlib import Path

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.repository import ProviderRepository, SiteRepository
from app.services.data_ingestion import (
    OPERATOR_MAPPING,
    create_providers_if_not_exist,
    seed_sites_from_csv,
)
from app.tests.factories import create_provider_factory


@pytest.mark.asyncio
async def test_create_providers_if_not_exist_creates_defaults(
    async_session: AsyncSession,
):
    provider_repo = ProviderRepository()

    await create_providers_if_not_exist(async_session)

    providers = await provider_repo.get_multi(async_session=async_session)

    assert len(providers) == len(OPERATOR_MAPPING)


@pytest.mark.asyncio
async def test_create_providers_if_not_exist_skips_existing(
    async_session: AsyncSession,
):
    provider_repo = ProviderRepository()

    await create_provider_factory()

    await create_providers_if_not_exist(async_session)

    existing_providers = await provider_repo.get_multi(
        async_session=async_session
    )

    assert len(existing_providers) > 0


@pytest.mark.asyncio
async def test_seed_sites_from_csv_inserts_transformed_coordinates(
    async_session: AsyncSession,
    mock_csv_file_path: Path,
    mock_csv_rows: list[dict[str, str]],
):
    provider_repo = ProviderRepository()
    site_repo = SiteRepository()

    await create_providers_if_not_exist(async_session)

    existing_providers = await provider_repo.get_multi(
        async_session=async_session,
    )
    provider_map = {}
    for provider in existing_providers:
        provider_map[provider.mobile_network_code] = provider.id

    await seed_sites_from_csv(
        async_session=async_session,
        csv_file_path=str(mock_csv_file_path),
    )

    existing_sites = await site_repo.get_multi(
        async_session=async_session,
    )

    sites_by_provider_id = {site.provider_id: site for site in existing_sites}

    assert len(existing_sites) == len(mock_csv_rows)

    for row in mock_csv_rows:
        provider_id = provider_map[row["Operateur"]]
        site = sites_by_provider_id[provider_id]
        assert site.has_2g is (row["2G"] == "1")
        assert site.has_3g is (row["3G"] == "1")
        assert site.has_4g is (row["4G"] == "1")
