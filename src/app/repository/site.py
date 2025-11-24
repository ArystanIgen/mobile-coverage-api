from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

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
    ) -> list[SiteModel]:
        stmt = (
            select(self.model)
            .options(joinedload(self.model.provider))
            .where(
                and_(
                    self.model.latitude >= latitude,
                    self.model.latitude <= latitude,
                    self.model.longitude >= longitude,
                    self.model.longitude <= longitude,
                )
            )
        )

        query = await async_session.execute(stmt)
        return query.scalars().all()
