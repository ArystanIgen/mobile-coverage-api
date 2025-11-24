from pydantic import BaseModel, Field


class SiteCreate(BaseModel):
    provider_id: int = Field(..., description="Provider ID")
    longitude: float = Field(..., description="Longitude of the site")
    latitude: float = Field(..., description="Latitude of the site")

    has_2g: bool = Field(..., description="Does the site have 2G coverage?")
    has_3g: bool = Field(..., description="Does the site have 3G coverage?")
    has_4g: bool = Field(..., description="Does the site have 4G coverage?")


class SiteUpdate(SiteCreate):
    pass
