from beanie import PydanticObjectId
from pydantic import BaseModel, Field


class BasicInfo(BaseModel):
    id: PydanticObjectId = Field(alias="_id")
    name: str


class Registration(BaseModel):
    guest: BasicInfo
    event: BasicInfo


class UnRegistraion(BaseModel):
    guest_id: PydanticObjectId = Field(alias="guestId")
    event_id: PydanticObjectId = Field(alias="eventId")
