from beanie import PydanticObjectId
from pydantic import BaseModel, ConfigDict, Field


class BasicRegistrationInfo(BaseModel):
    # We have to set it to populate_by_name=True to be able to use alias in nested models
    model_config = ConfigDict(populate_by_name=True)

    id: PydanticObjectId = Field(alias="_id")
    name: str


class Registration(BaseModel):
    guest_id: PydanticObjectId = Field(alias="guestId")
    event_id: PydanticObjectId = Field(alias="eventId")


class UnRegistraion(BaseModel):
    guest_id: PydanticObjectId = Field(alias="guestId")
    event_id: PydanticObjectId = Field(alias="eventId")
