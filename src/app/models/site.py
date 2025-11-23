from app.db.base import BaseModel
from sqlalchemy import Column, Boolean, ForeignKey, Float
from sqlalchemy.orm import relationship


class SiteModel(BaseModel):
    __tablename__ = "site"

    provider_id = Column(ForeignKey("provider.id"), nullable=False)

    provider = relationship("Provider", back_populates="sites")

    x_l93 = Column(Float, nullable=False)
    y_l93 = Column(Float, nullable=False)

    has_2g = Column(Boolean, nullable=False, default=False)
    has_3g = Column(Boolean, nullable=False, default=False)
    has_4g = Column(Boolean, nullable=False, default=False)
