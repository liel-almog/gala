from beanie import Document, PydanticObjectId
from pydantic import BaseModel, Field


class Guest(BaseModel):
    name: str
    events: list[PydanticObjectId] | None = Field(default=[])
    is_vip: bool | None = Field(alias="isVip", default=False)
    age: int = Field(ge=18)


class GuestDocument(Document, Guest):
    pass
