from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class ProviderModel(BaseModel):
    __tablename__ = "provider"

    mobile_network_code = Column(String(10), unique=True, nullable=False)
    name = Column(String(50), unique=True, nullable=False)
    sites = relationship(
        "SiteModel",
        back_populates="provider",
        cascade="all, delete-orphan",
    )
