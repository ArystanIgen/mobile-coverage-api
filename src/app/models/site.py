from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models import ProviderModel


class SiteModel(BaseModel):
    __tablename__ = "site"

    provider_id: Mapped[int] = mapped_column(
        ForeignKey("provider.id"),
        nullable=False
    )
    provider: Mapped["ProviderModel"] = relationship(
        "ProviderModel",
        back_populates="sites",
    )
    longitude: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )
    latitude: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )
    has_2g: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )
    has_3g: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )
    has_4g: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )
