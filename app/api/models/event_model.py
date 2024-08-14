import datetime as dt

from beanie import Document
from pydantic import BaseModel, Field

from app.api.models.register_model import BasicRegistrationInfo
from app.core.utils.partial import partial_model


class Event(BaseModel):
    name: str
    dress_code: str = Field(alias="dressCode")
    location: str
    guests: list[BasicRegistrationInfo] | None = Field(default=[])
    date: dt.datetime  # Date does not have be greater than today
    is_vip_event: bool = Field(alias="isVipEvent", default=False)


@partial_model()
class PartialEvent(Event):
    pass


class EventDocument(Document, Event):
    pass

    class Settings:
        name = "events"


# Please keep notice that the order of inheritance is important
class PartialEventDocument(PartialEvent, EventDocument):
    pass


class EventOnlyWithGuests(BaseModel):
    guests: list[BasicRegistrationInfo] | None = Field(default=[])
