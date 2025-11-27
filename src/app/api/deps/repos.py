from typing import Annotated

from fastapi import Depends

from app.repository import SiteRepository


def get_site_repo() -> SiteRepository:
    return SiteRepository()


SiteRepoDep = Annotated[SiteRepository, Depends(get_site_repo)]
