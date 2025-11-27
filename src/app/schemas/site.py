from geoalchemy2.elements import WKTElement
from pydantic import BaseModel, ConfigDict, Field, model_validator


class SiteCreate(BaseModel):
    provider_id: int = Field(..., description="Provider ID")
    longitude: float = Field(..., description="Longitude of the site")
    latitude: float = Field(..., description="Latitude of the site")

    has_2g: bool = Field(..., description="Does the site have 2G coverage?")
    has_3g: bool = Field(..., description="Does the site have 3G coverage?")
    has_4g: bool = Field(..., description="Does the site have 4G coverage?")

    location: WKTElement | None = Field(
        default=None, description="Location of the site"
    )
    model_config = ConfigDict(arbitrary_types_allowed=True)

    @model_validator(mode="after")
    def set_location(self):
        if self.location is None:
            self.location = WKTElement(
                f"POINT({self.longitude} {self.latitude})",
                srid=4326,
            )
        return self


class SiteUpdate(SiteCreate):
    pass
