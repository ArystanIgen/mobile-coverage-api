from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import func

from app.core.config import CONFIG
from app.models import ProviderModel, SiteModel
from app.repository.base import BaseRepository
from app.schemas.site import SiteCoverageRow, SiteCreate, SiteUpdate


class SiteRepository(BaseRepository[SiteModel, SiteCreate, SiteUpdate]):
    model = SiteModel

    async def get_nearby_sites(
        self,
        async_session: AsyncSession,
        *,
        longitude: float,
        latitude: float,
    ) -> list[SiteCoverageRow]:
        # PostGIS point from lat/lon (WGS84)
        postgis_point = func.ST_SetSRID(
            func.ST_MakePoint(longitude, latitude), 4326
        )

        is_within_radius = func.ST_DWithin(
            self.model.location,
            postgis_point,
            CONFIG.search_radius_meters,
        )

        stmt = (
            select(
                ProviderModel.name.label("provider"),
                func.bool_or(self.model.has_2g).label("g2"),
                func.bool_or(self.model.has_3g).label("g3"),
                func.bool_or(self.model.has_4g).label("g4"),
            )
            .select_from(self.model)
            .join(
                ProviderModel,
                ProviderModel.id == self.model.provider_id,
            )
            .where(is_within_radius)
            .group_by(ProviderModel.name)
        )

        result = await async_session.execute(stmt)
        return [
            SiteCoverageRow(row.provider, row.g2, row.g3, row.g4)
            for row in result
        ]
