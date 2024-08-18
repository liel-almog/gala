from beanie import Document
from pydantic import BaseModel


class Organizer(BaseModel):
    name: str


class OrganizerDocument(Document, Organizer):
    pass

    class Settings:
        name = "organizers"
