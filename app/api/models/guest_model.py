from beanie import Document
from pydantic import BaseModel, Field, ValidationInfo, field_validator

from app.api.models.register_model import BasicRegistrationInfo
from app.core.utils.partial import partial_model


class Guest(BaseModel):
    name: str
    events: list[BasicRegistrationInfo] | None = Field(default=[])
    is_vip: bool | None = Field(alias="isVip", default=False)
    age: int = Field(ge=18)
    custom_requirements: str | None = Field(
        default=None,
        alias="customRequirements",
        validate_default=True,
    )

    @field_validator("custom_requirements")
    @classmethod
    def validate_vip_custom_requirements(cls, v: str, info: ValidationInfo):
        if not info.data.get("is_vip") and v:
            raise ValueError("Custom requirements can be set only for VIP guests")

        return v


class GuestDocument(Document, Guest):
    pass

    class Settings:
        name = "guests"


@partial_model()
class PartialGuestDocument(GuestDocument):
    pass


class GuestOnlyWithEvents(BaseModel):
    events: list[BasicRegistrationInfo] | None = Field(default=[])
