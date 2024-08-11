from beanie import Document, PydanticObjectId
from pydantic import BaseModel, Field

from app.core.utils.partial import partial_model


class Guest(BaseModel):
    name: str
    events: list[PydanticObjectId] | None = Field(default=[])
    is_vip: bool | None = Field(alias="isVip", default=False)
    age: int = Field(ge=18)


class GuestDocument(Document, Guest):
    pass

    class Settings:
        name = "guests"


@partial_model()
class PartialGuestDocument(GuestDocument):
    pass
