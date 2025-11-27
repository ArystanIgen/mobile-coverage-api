from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlalchemy.sql import func

from app.models import SiteModel
from app.repository.base import BaseRepository
from app.schemas.site import SiteCreate, SiteUpdate


class SiteRepository(BaseRepository[SiteModel, SiteCreate, SiteUpdate]):
    model = SiteModel

    async def get_nearby_sites(
        self,
        async_session: AsyncSession,
        *,
        longitude: float,
        latitude: float,
        radius_m: int = 1000,
    ) -> list[SiteModel]:
        # Build a PostGIS point from lat/lon (WGS84)
        postgis_point = func.ST_SetSRID(
            func.ST_MakePoint(longitude, latitude), 4326
        )

        stmt = (
            select(self.model)
            .options(joinedload(self.model.provider))
            # checks whether
            # two geometries are within a certain distance of each other
            # (in this case, it is 1000 m)
            .where(
                func.ST_DWithin(
                    self.model.location,
                    postgis_point,
                    radius_m,
                )
            )
        )

        query = await async_session.execute(stmt)
        return list(query.scalars().all())
