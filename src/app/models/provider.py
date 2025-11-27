from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models import SiteModel


class ProviderModel(BaseModel):
    __tablename__ = "provider"

    mobile_network_code: Mapped[str] = mapped_column(
        String(10),
        unique=True,
        nullable=False,
    )
    name: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
    )
    sites: Mapped[list["SiteModel"]] = relationship(
        "SiteModel",
        back_populates="provider",
        cascade="all, delete-orphan",
    )
