from sqlalchemy import Boolean, Column, Float, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class SiteModel(BaseModel):
    __tablename__ = "site"

    provider_id = Column(ForeignKey("provider.id"), nullable=False)

    provider = relationship("ProviderModel", back_populates="sites")

    longitude = Column(Float, nullable=False)
    latitude = Column(Float, nullable=False)

    has_2g = Column(Boolean, nullable=False, default=False)
    has_3g = Column(Boolean, nullable=False, default=False)
    has_4g = Column(Boolean, nullable=False, default=False)
