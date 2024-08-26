from beanie import Document, PydanticObjectId
from pydantic import BaseModel, Field, ValidationInfo, field_validator
from typing import Optional

from app.api.models.register_model import BasicRegistrationInfo
from app.core.utils.partial import partial_model


class CustomRequest(BaseModel):
    id: PydanticObjectId = Field(default_factory=PydanticObjectId, alias="_id")
    fulfilled: bool = Field(default=False)
    description: str = Field(max_length=100)


class Guest(BaseModel):
    name: str
    events: Optional[list[BasicRegistrationInfo]] = Field(default=[])
    is_vip: Optional[bool] = Field(alias="isVip", default=False)
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


@partial_model()
class PartialGuest(Guest):
    pass


class GuestDocument(Document, Guest):
    pass

    class Settings:
        name = "guests"


class GuestOnlyWithEvents(BaseModel):
    events: list[BasicRegistrationInfo] = Field(default=[])
