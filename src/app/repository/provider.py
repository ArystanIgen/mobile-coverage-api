from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import ProviderModel
from app.repository.base import BaseRepository
from app.schemas.provider import ProviderCreate, ProviderUpdate


class ProviderRepository(
    BaseRepository[ProviderModel, ProviderCreate, ProviderUpdate]
):
    model = ProviderModel

    async def get_provider_by_mobile_network_code(
        self,
        async_session: AsyncSession,
        *,
        mobile_network_code: str,
    ) -> ProviderModel | None:
        stmt = select(self.model).where(
            self.model.mobile_network_code == mobile_network_code,
        )
        query = await async_session.execute(stmt)
        return query.scalar()
