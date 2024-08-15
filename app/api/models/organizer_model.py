from enum import Enum, auto
from beanie import Document, PydanticObjectId
from pydantic import BaseModel, Field

from app.core.utils.partial import partial_model


class EventRoles(Enum):
    ORGANIZER = auto()
    DJ = auto()
    PHOTOGRAPHER = auto()
    BARTENDER = auto()
    SECURITY = auto()
    WAITER = auto()
    CLEANER = auto()
    CATERER = auto()
    HOST = auto()
    PERFORMER = auto()
    MANAGER = auto()


class Organizer(BaseModel):
    name: str
    role: EventRoles
    events: list[PydanticObjectId] | None = Field(default=[])


@partial_model()
class PartialOrganizer(Organizer):
    pass


class OrganizerDocument(Document, Organizer):
    pass

    class Settings:
        name = "organizers"


class PartialOrganizerDocument(PartialOrganizer, OrganizerDocument):
    pass
