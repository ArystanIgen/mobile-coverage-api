from pydantic import BaseModel, Field


class ProviderCreate(BaseModel):
    mobile_network_code: str = Field(..., description="Mobile Network Code")
    name: str = Field(..., description="Provider Name")


class ProviderUpdate(BaseModel):
    pass
