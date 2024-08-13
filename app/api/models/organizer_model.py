from enum import Enum, auto
from beanie import Document
from pydantic import BaseModel


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


class OrganizerDocument(Document, Organizer):
    pass

    class Settings:
        name = "organizers"
