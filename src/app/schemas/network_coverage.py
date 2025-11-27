
from pydantic import BaseModel, ConfigDict, Field


class NetworkAvailability(BaseModel):
    g2: bool = Field(..., description="2G coverage", alias="2G")
    g3: bool = Field(..., description="3G coverage", alias="3G")
    g4: bool = Field(..., description="4G coverage", alias="4G")

    model_config = ConfigDict(populate_by_name=True)


OperatorsAvailability = dict[str, NetworkAvailability]
