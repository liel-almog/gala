import datetime as dt

from beanie import Document, PydanticObjectId
from pydantic import BaseModel, Field

from app.api.models.register_model import BasicRegistrationInfo
from app.core.utils.partial import partial_model


class Event(BaseModel):
    name: str
    dress_code: str = Field(alias="dressCode")
    location: str
    guests: list[BasicRegistrationInfo] = Field(default=[])
    date: dt.datetime  # Date does not have be greater than today
    is_vip_event: bool = Field(alias="isVipEvent", default=False)
    organizers: list[PydanticObjectId] = Field(default=[])


@partial_model()
class PartialEvent(Event):
    pass


class EventDocument(Document, Event):
    pass

    class Settings:
        name = "events"


@partial_model()
class PartialEventDocument(EventDocument):
    pass


class EventOnlyWithGuests(BaseModel):
    guests: list[BasicRegistrationInfo] = Field(default=[])
