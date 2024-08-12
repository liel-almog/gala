from beanie import PydanticObjectId
from pydantic import BaseModel, Field


class BasicRegistrationInfo(BaseModel):
    id: PydanticObjectId = Field(serialization_alias="_id")
    name: str


class Registration(BaseModel):
    guest_id: PydanticObjectId = Field(alias="guestId")
    event_id: PydanticObjectId = Field(alias="eventId")


class UnRegistraion(BaseModel):
    guest_id: PydanticObjectId = Field(alias="guestId")
    event_id: PydanticObjectId = Field(alias="eventId")
