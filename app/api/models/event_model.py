import datetime
from beanie import Document, PydanticObjectId
from pydantic import BaseModel, Field


class Event(BaseModel):
    name: str
    dress_code: str = Field(alias="dressCode")
    location: str
    guests: list[PydanticObjectId] | None = Field(default=[])
    date: datetime.datetime


class EventDocument(Document, BaseModel):
    pass
