from typing import Annotated

from fastapi import Depends

from app.repository import ProviderRepository, SiteRepository


def get_site_repo() -> SiteRepository:
    return SiteRepository()


def get_provider_repo() -> ProviderRepository:
    return ProviderRepository()


ProviderRepoDep = Annotated[ProviderRepository, Depends(get_provider_repo)]
SiteRepoDep = Annotated[SiteRepository, Depends(get_site_repo)]
