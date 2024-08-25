from enum import Enum
from beanie import Document
from pydantic import BaseModel

from app.core.utils.partial import partial_model


class OrganizerRoles(str, Enum):
    ORGANIZER = "Organizer"
    DJ = "DJ"
    PHOTOGRAPHER = "PhotoGrapher"
    BARTENDER = "Bartender"
    SECURITY = "Security"
    WAITER = "Waiter"
    CLEANER = "Cleaner"
    CATERER = "Caterer"
    HOST = "Host"
    PERFORMER = "Performer"
    MANAGER = "Manager"


class Organizer(BaseModel):
    name: str
    role: OrganizerRoles


@partial_model()
class PartialOrganizer(Organizer):
    pass


class OrganizerDocument(Document, Organizer):
    pass

    class Settings:
        name = "organizers"
