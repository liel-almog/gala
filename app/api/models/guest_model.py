from typing import Optional
from beanie import Document
from pydantic import BaseModel, Field

from app.api.models.register_model import BasicRegistrationInfo
from app.core.utils.partial import partial_model


class Guest(BaseModel):
    name: str
    events: Optional[list[BasicRegistrationInfo]] = Field(default=[])
    is_vip: Optional[bool] = Field(alias="isVip", default=False)
    age: int = Field(ge=18)


@partial_model()
class PartialGuest(Guest):
    pass


class GuestDocument(Document, Guest):
    pass

    class Settings:
        name = "guests"


class GuestOnlyWithEvents(BaseModel):
    events: list[BasicRegistrationInfo] = Field(default=[])
