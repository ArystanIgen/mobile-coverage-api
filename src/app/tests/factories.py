from typing import Any, Awaitable, cast

import factory
from factory.alchemy import SQLAlchemyModelFactory
from geoalchemy2.elements import WKTElement

from app.models import ProviderModel, SiteModel


class AsyncSQLAlchemyModelFactory(SQLAlchemyModelFactory):
    @classmethod
    async def _create(cls, model_class, *args, **kwargs):
        instance = super()._create(model_class, *args, **kwargs)
        async with cls._meta.sqlalchemy_session as session:  # type: ignore[attr-defined]
            await session.commit()
        return instance


class ProviderFactory(AsyncSQLAlchemyModelFactory):
    class Meta:
        model = ProviderModel

    name = factory.Sequence(lambda n: f"Provider {n}")
    mobile_network_code = factory.Faker(
        "bothify", text="###", letters="0123456789"
    )


class SiteFactory(AsyncSQLAlchemyModelFactory):
    class Meta:
        model = SiteModel

    provider = factory.SubFactory(ProviderFactory)
    longitude = factory.Faker("longitude")
    latitude = factory.Faker("latitude")
    location = factory.LazyAttribute(
        lambda obj: WKTElement(
            f"POINT({obj.longitude} {obj.latitude})",
            srid=4326,
        )
    )
    has_2g = factory.Faker("pybool")
    has_3g = factory.Faker("pybool")
    has_4g = factory.Faker("pybool")


async def create_provider_factory(**kwargs: Any) -> ProviderModel:
    return await cast(Awaitable[ProviderModel], ProviderFactory(**kwargs))


async def create_site_factory(**kwargs: Any) -> SiteModel:
    return await cast(Awaitable[SiteModel], SiteFactory(**kwargs))
