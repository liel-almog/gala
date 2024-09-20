from beanie import Document, PydanticObjectId
from pydantic import BaseModel, Field, ValidationInfo, field_validator


class CustomRequest(BaseModel):
    id: PydanticObjectId = Field(alias="_id")
    fulfilled: bool = Field(default=False)
    description: str = Field(max_length=100)


class Guest(BaseModel):
    name: str
    is_vip: bool | None = Field(alias="isVip", default=False)
    age: int = Field(ge=18)
    custom_requests: list[CustomRequest] | None = Field(
        default=[], alias="customRequests"
    )

    @field_validator("custom_requests")
    @classmethod
    def validate_vip_custom_requests(cls, v: str, info: ValidationInfo):
        if not info.data.get("is_vip") and bool(v):
            raise ValueError("Custom requests can be set only for VIP guests")

        return v


class GuestDocument(Guest, Document):
    class Settings:
        name = "guests"
