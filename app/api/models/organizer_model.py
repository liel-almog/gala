from enum import Enum, auto
from beanie import Document
from pydantic import BaseModel

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


@partial_model()
class PartialOrganizer(Organizer):
    pass


class OrganizerDocument(Document, Organizer):
    pass

    class Settings:
        name = "organizers"
