# event_service.py
from typing import Annotated

from beanie import PydanticObjectId, UpdateResponse
from beanie.operators import AddToSet, Pull, Set
from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClientSession
from pymongo.results import UpdateResult

from app.api.errors.event_not_found import EventNotFound
from app.api.models.event_model import Event, EventOnlyWithGuests
from app.api.models.guest_model import GuestDocument
from app.api.models.register_model import BasicRegistrationInfo
from app.api.repositories.event_repository import CommonEventRepository, EventRepository


class EventService:
    _event_repository: EventRepository

    def __init__(self, event_repo: EventRepository) -> None:
        self._event_repository = event_repo

    async def get_all(self):
        return await self._event_repository.find_all()

    async def get_one_by_id(self, id: PydanticObjectId):
        return self._event_repository.find_one_by_id(id)

    async def create(self, event: Event):
        return await self._event_repository.create(event)

    async def update_one_by_id(self, id: PydanticObjectId, event: ParitalEve):
        return await self._event_repository.update_one_by_id(id, event)

    async def delete_one_by_id(
        self,
        id: PydanticObjectId,
        session: AsyncIOMotorClientSession | None = None,
    ):
        res = await Event.find_one(Event.id == id).delete_one(session=session)

        if not res.deleted_count:
            raise EventNotFound(f"Event with id {id} not found")

        return res

    async def remove_guest_from_all_events(
        self,
        guest_id: PydanticObjectId,
        session: AsyncIOMotorClientSession | None = None,
    ):
        return await Event.find_many({"guests._id": guest_id}).update_many(
            Pull({Event.guests: {GuestDocument.id: guest_id}}), session=session
        )

    async def get_guests_by_event_id(self, event_id: PydanticObjectId):
        guests = await Event.find_one(
            Event.id == event_id,
            projection_model=EventOnlyWithGuests,
        )

        if not guests:
            raise EventNotFound(f"Event with id {event_id} not found")

        return guests

    async def remove_guest_from_event(
        self,
        event_id: PydanticObjectId,
        guest_id: PydanticObjectId,
        session: AsyncIOMotorClientSession | None = None,
    ) -> UpdateResult:
        res = await Event.find_one(Event.id == event_id).update_one(
            Pull({Event.guests: {GuestDocument.id: guest_id}}), session=session
        )

        if not res.matched_count:
            raise EventNotFound(f"Event with id {event_id} not found")

        return res

    async def add_guest_to_event(
        self,
        event_id: PydanticObjectId,
        guest_basic_info: BasicRegistrationInfo,
        session: AsyncIOMotorClientSession | None = None,
    ) -> UpdateResult:
        res = await Event.find_one(Event.id == event_id).update_one(
            AddToSet({Event.guests: guest_basic_info}), session=session
        )

        if not res.matched_count:
            raise EventNotFound(f"Event with id {event_id} not found")

        return res


def get_event_service(event_repo: CommonEventRepository):
    return EventService(event_repo)


CommonEventService = Annotated[EventService, Depends(get_event_service, use_cache=True)]
