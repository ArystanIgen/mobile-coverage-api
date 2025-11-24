from app.models import SiteModel
from app.repository.base import BaseRepository
from app.schemas.site import SiteCreate, SiteUpdate


class SiteRepository(BaseRepository[SiteModel, SiteCreate, SiteUpdate]):
    model = SiteModel
