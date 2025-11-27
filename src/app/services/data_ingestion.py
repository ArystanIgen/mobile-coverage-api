import csv

import pyproj
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import CONFIG
from app.db.session import async_session_factory
from app.models import ProviderModel
from app.repository import ProviderRepository, SiteRepository
from app.schemas.provider import ProviderCreate
from app.schemas.site import SiteCreate

OPERATOR_MAPPING = {
    "20801": "orange",
    "20810": "sfr",
    "20815": "free",
    "20820": "bouygues",
}

TRANSFORMER = pyproj.Transformer.from_crs(
    "+proj=lcc "
    "+lat_1=49 "
    "+lat_2=44 "
    "+lat_0=46.5 "
    "+lon_0=3 "
    "+x_0=700000 "
    "+y_0=6600000 "
    "+ellps=GRS80 "
    "+towgs84=0,0,0,0,0,0,0 "
    "+units=m "
    "+no_defs",
    "+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs",
    always_xy=True,
)

provider_repo = ProviderRepository()
site_repo = SiteRepository()


def parse_float(value: str) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


async def create_providers_if_not_exist(
    async_session: AsyncSession,
):
    existing_providers = await provider_repo.get_multi(
        async_session=async_session,
    )

    if existing_providers:
        logger.info("Providers already exist. Skipping site seeding.")
        return

    for mobile_network_code, name in OPERATOR_MAPPING.items():
        await provider_repo.create(
            async_session=async_session,
            obj_in=ProviderCreate(
                mobile_network_code=mobile_network_code,
                name=name,
            ),
        )
    logger.info("Providers created")


async def seed_sites_from_csv(
    async_session: AsyncSession,
    csv_file_path: str | None = None,
) -> None:
    existing_sites = await site_repo.get_multi(async_session=async_session)
    if existing_sites:
        logger.info("Sites already exist. Skipping seeding.")
        return

    target_csv = csv_file_path or CONFIG.sites_csv_file_path

    logger.info(f"Reading CSV from {target_csv}...")

    sites_batch = []
    processed_count = 0
    batch_size = 5000

    fetched_providers: list[ProviderModel] = await provider_repo.get_multi(
        async_session=async_session,
    )

    provider_map = {
        provider.mobile_network_code: provider.id
        for provider in fetched_providers
    }

    with open(target_csv, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=";")

        for row in reader:
            mobile_network_code = row["Operateur"]
            parsed_x = parse_float(row.get("x"))
            parsed_y = parse_float(row.get("y"))

            provider_id = provider_map.get(mobile_network_code)
            if provider_id and parsed_x and parsed_y:
                longitude, latitude = TRANSFORMER.transform(parsed_x, parsed_y)
                sites_batch.append(
                    SiteCreate(
                        provider_id=provider_id,
                        latitude=latitude,
                        longitude=longitude,
                        has_2g=row["2G"] == "1",
                        has_3g=row["3G"] == "1",
                        has_4g=row["4G"] == "1",
                    )
                )
                if len(sites_batch) >= batch_size:
                    await site_repo.create_bulk(
                        async_session=async_session,
                        objs_in=sites_batch,
                    )
                    processed_count += len(sites_batch)
                    sites_batch = []
        if sites_batch:
            await site_repo.create_bulk(
                async_session=async_session,
                objs_in=sites_batch,
            )
            processed_count += len(sites_batch)
        logger.info(f"Done! Added total of {processed_count} Sites.")


async def seed_providers_and_sites() -> None:
    async with async_session_factory() as async_session:
        await create_providers_if_not_exist(
            async_session=async_session,
        )

        await seed_sites_from_csv(async_session=async_session)