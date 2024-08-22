from typing import Annotated

from beanie import PydanticObjectId, UpdateResponse
from beanie.operators import AddToSet, Pull, Set
from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClientSession
from pymongo.results import UpdateResult

from app.api.errors.guest_not_found import GuestNotFound
from app.api.models.event_model import EventDocument
from app.api.models.guest_model import (
    Guest,
    GuestDocument,
    GuestOnlyWithEvents,
    PartialGuest,
)
from app.api.models.register_model import BasicRegistrationInfo


class GuestRepository:
    async def find_all(self):
        return await GuestDocument.find_all().to_list()

    async def find_one_by_id(self, id: PydanticObjectId):
        guest = await GuestDocument.get(id)
        if not guest:
            raise GuestNotFound(f"Guest with id {id} not found")

        return guest

    async def create(self, guest: Guest):
        guest_to_insert = GuestDocument(**guest.model_dump(by_alias=True))
        return await guest_to_insert.save()

    async def update_one_by_id(self, id: PydanticObjectId, guest: PartialGuest):
        guest_dict = guest.model_dump(exclude_unset=True, by_alias=True)
        res = await GuestDocument.find_one(GuestDocument.id == id).update_one(
            Set(guest_dict), response_type=UpdateResponse.UPDATE_RESULT
        )

        if not res.matched_count:
            raise GuestNotFound(f"Guest with id {id} not found")

        return res

    async def delete_one_by_id(
        self, id: PydanticObjectId, session: AsyncIOMotorClientSession | None = None
    ):
        res = await GuestDocument.find_one(GuestDocument.id == id).delete_one(
            session=session
        )

        if not res.deleted_count:
            raise GuestNotFound(f"Guest with id {id} not found")

        return res

    async def remove_event_from_all_guests(
        self,
        event_id: PydanticObjectId,
        session: AsyncIOMotorClientSession | None = None,
    ):
        return await GuestDocument.find_many({"events._id": event_id}).update_many(
            Pull({GuestDocument.events: {EventDocument.id: event_id}}), session=session
        )

    async def remove_event_from_guest(
        self,
        guest_id: PydanticObjectId,
        event_id: PydanticObjectId,
        session: AsyncIOMotorClientSession | None = None,
    ) -> UpdateResult:
        res = await GuestDocument.find_one(GuestDocument.id == guest_id).update_one(
            Pull({GuestDocument.events: {EventDocument.id: event_id}}),
            session=session,
            response_type=UpdateResponse.UPDATE_RESULT,
        )

        if not res.matched_count:
            raise GuestNotFound(f"Guest with id {guest_id} not found")

        return res

    async def find_guest_events_by_id(self, id: PydanticObjectId):
        guest_only_with_events = await GuestDocument.find_one(
            GuestDocument.id == id,
            projection_model=GuestOnlyWithEvents,
        )

        if not guest_only_with_events:
            raise GuestNotFound(f"Guest with id {id} not found")

        return guest_only_with_events

    async def add_event_to_guest(
        self,
        guest_id: PydanticObjectId,
        event_basic_info: BasicRegistrationInfo,
        session: AsyncIOMotorClientSession | None = None,
    ):
        res = await GuestDocument.find_one(GuestDocument.id == guest_id).update_one(
            AddToSet({GuestDocument.events: event_basic_info}), session=session
        )

        if not res.matched_count:
            raise GuestNotFound(f"Guest with id {guest_id} not found")

        return res


def get_guest_repository():
    return GuestRepository()


CommonGuestRepository = Annotated[GuestRepository, Depends(get_guest_repository)]
