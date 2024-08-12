# event_service.py
from typing import Annotated

from beanie import PydanticObjectId, UpdateResponse
from beanie.operators import AddToSet, Pull, Set
from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClientSession
from pymongo.results import UpdateResult

from app.api.errors.event_not_found import EventNotFound
from app.api.models.event_model import EventDocument
from app.api.models.guest_model import GuestDocument
from app.api.models.register_model import BasicRegistrationInfo


class EventService:
    def __init__(self) -> None:
        pass

    async def get_all(self):
        return await EventDocument.find_all().to_list()

    async def get_one_by_id(self, id: PydanticObjectId):
        event = await EventDocument.find_one(EventDocument.id == id)
        if not event:
            raise EventNotFound(f"Event not found with id {id}")

        return event

    async def create(self, event: EventDocument):
        return await EventDocument.insert_one(event)

    async def update_one_by_id(
        self, id: PydanticObjectId, event: EventDocument
    ) -> UpdateResult:
        event_dict = event.model_dump(exclude_unset=True, by_alias=True)
        res = await EventDocument.find_one(EventDocument.id == id).update_one(
            Set(event_dict), response_type=UpdateResponse.UPDATE_RESULT
        )

        if not res.matched_count:
            raise EventNotFound(f"Event not found with id {id}")

        return res

    async def delete_one_by_id(
        self,
        id: PydanticObjectId,
        session: AsyncIOMotorClientSession | None = None,
    ):
        return await EventDocument.find_one(EventDocument.id == id).delete_one(
            session=session
        )

    async def remove_guest_from_all_events(
        self,
        guest_id: PydanticObjectId,
        session: AsyncIOMotorClientSession | None = None,
    ):
        return await EventDocument.find_many({"guests._id": guest_id}).update_many(
            Pull({EventDocument.guests: {GuestDocument.id: guest_id}}), session=session
        )

    async def remove_guest_from_event(
        self,
        event_id: PydanticObjectId,
        guest_id: PydanticObjectId,
        session: AsyncIOMotorClientSession | None = None,
    ) -> UpdateResult:
        res = await EventDocument.find_one(EventDocument.id == event_id).update_one(
            Pull({EventDocument.guests: {GuestDocument.id: guest_id}}), session=session
        )

        if not res.matched_count:
            raise EventNotFound(f"Event not found with id {event_id}")

        return res

    async def add_guest_to_event(
        self,
        event_id: PydanticObjectId,
        guest_basic_info: BasicRegistrationInfo,
        session: AsyncIOMotorClientSession | None = None,
    ) -> UpdateResult:
        res = await EventDocument.find_one(EventDocument.id == event_id).update_one(
            AddToSet({EventDocument.guests: guest_basic_info}), session=session
        )

        if not res.matched_count:
            raise EventNotFound(f"Event not found with id {event_id}")

        return res


def get_event_service():
    return EventService()


CommonEventService = Annotated[EventService, Depends(get_event_service, use_cache=True)]
