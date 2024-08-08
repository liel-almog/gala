from beanie import Document, PydanticObjectId
from pydantic import Field


class Event(Document):
    name: str
    guests: list[PydanticObjectId] | None = Field(default=[])


class Guest(Document):
    name: str
    events: list[PydanticObjectId] | None = Field(default=[])
