from app.db.base import BaseModel

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class ProviderModel(BaseModel):
    __tablename__ = "provider"

    mnc = Column(String(10), unique=True, nullable=False)
    name = Column(String(50), unique=True, nullable=False)
    sites = relationship(
        "SiteModel",
        back_populates="provider",
        cascade="all, delete-orphan",
    )
