import datetime
from beanie import Document, PydanticObjectId
from pydantic import BaseModel, Field

from app.core.utils.partial import partial_model


class Event(BaseModel):
    name: str
    dress_code: str = Field(alias="dressCode")
    location: str
    guests: list[PydanticObjectId] | None = Field(default=[])
    date: datetime.datetime  # Date does not have be greater than today


class EventDocument(Document, Event):
    pass

    class Settings:
        name = "events"


@partial_model()
class PartialEventDocument(EventDocument):
    pass
