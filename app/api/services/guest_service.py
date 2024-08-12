# guest_service.py
from typing import Annotated

from beanie import PydanticObjectId, UpdateResponse
from beanie.operators import Pull, Set, AddToSet
from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClientSession
from pymongo.results import UpdateResult

from app.api.errors.guest_not_found import GuestNotFound
from app.api.models.event_model import EventDocument
from app.api.models.guest_model import GuestDocument
from app.api.models.register_model import BasicRegistrationInfo


class GuestService:
    def __init__(self) -> None:
        pass

    async def get_all(self):
        return await GuestDocument.find_all().to_list()

    async def get_one_by_id(self, id: PydanticObjectId):
        guest = await GuestDocument.find_one(GuestDocument.id == id)
        if not guest:
            raise GuestNotFound(f"Guest not found with id {id}")

        return guest

    async def create(self, guest: GuestDocument):
        return await GuestDocument.insert_one(guest)

    async def update_one_by_id(
        self, id: PydanticObjectId, guest: GuestDocument
    ) -> UpdateResult:
        guest_dict = guest.model_dump(exclude_unset=True, by_alias=True)
        return await GuestDocument.find_one(GuestDocument.id == id).update_one(
            Set(guest_dict), response_type=UpdateResponse.UPDATE_RESULT
        )

    async def delete_one_by_id(
        self, id: PydanticObjectId, session: AsyncIOMotorClientSession | None = None
    ):
        return await GuestDocument.find_one(GuestDocument.id == id).delete_one(
            session=session
        )

    async def remove_event_from_all_guests(
        self,
        event_id: PydanticObjectId,
        session: AsyncIOMotorClientSession | None = None,
    ) -> UpdateResult:
        return await GuestDocument.find_many({"events._id": event_id}).update_many(
            Pull({GuestDocument.events: {EventDocument.id: event_id}}), session=session
        )

    async def remove_event_from_guest(
        self,
        guest_id: PydanticObjectId,
        event_id: PydanticObjectId,
        session: AsyncIOMotorClientSession | None = None,
    ) -> UpdateResult:
        return await GuestDocument.find_one(GuestDocument.id == guest_id).update_one(
            Pull({GuestDocument.events: {EventDocument.id: event_id}}), session=session
        )

    async def add_event_to_guest(
        self,
        guest_id: PydanticObjectId,
        event_basic_info: BasicRegistrationInfo,
        session: AsyncIOMotorClientSession | None = None,
    ) -> UpdateResult:
        return await GuestDocument.find_one(GuestDocument.id == guest_id).update_one(
            AddToSet({GuestDocument.events: event_basic_info}), session=session
        )


def get_guest_service():
    return GuestService()


CommonGuestService = Annotated[GuestService, Depends(get_guest_service, use_cache=True)]
