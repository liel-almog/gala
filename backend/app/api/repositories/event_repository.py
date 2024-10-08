from typing import Annotated, Optional

from beanie import PydanticObjectId, UpdateResponse
from beanie.operators import AddToSet, Pull, Set
from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClientSession
from pymongo.results import UpdateResult, DeleteResult

from app.api.errors.event_not_found import EventNotFound
from app.api.models.event_model import (
    Event,
    EventDocument,
    EventOnlyWithGuests,
    PartialEvent,
)
from app.api.models.guest_model import GuestDocument
from app.api.models.register_model import BasicRegistrationInfo


class EventRepository:
    async def find_all(self) -> list[EventDocument]:
        return await EventDocument.find_all().to_list()

    async def find_one_by_id(self, id: PydanticObjectId) -> EventDocument:
        event = await EventDocument.get(id)
        if not event:
            raise EventNotFound(f"Event with id {id} not found")

        return event

    async def create(self, event: Event) -> EventDocument:
        event_to_create = EventDocument(**event.model_dump())
        return await EventDocument.insert_one(event_to_create)

    async def update_one_by_id(
        self, id: PydanticObjectId, event: PartialEvent
    ) -> UpdateResult:
        event_dict = event.model_dump(exclude_unset=True, by_alias=True)
        res = await EventDocument.find_one(EventDocument.id == id).update_one(
            Set(event_dict), response_type=UpdateResponse.UPDATE_RESULT
        )

        if not res.matched_count:
            raise EventNotFound(f"Event with id {id} not found")

        return res

    async def delete_one_by_id(
        self, id: PydanticObjectId, session: AsyncIOMotorClientSession
    ) -> DeleteResult:
        res = await EventDocument.find_one(EventDocument.id == id).delete_one(
            session=session
        )

        if not res.deleted_count:
            raise EventNotFound(f"Event with id {id} not found")

        return res

    async def remove_guest_from_all_events(
        self,
        guest_id: PydanticObjectId,
        session: Optional[AsyncIOMotorClientSession] = None,
    ) -> UpdateResult:
        return await EventDocument.find_many({"guests._id": guest_id}).update_many(
            Pull({EventDocument.guests: {GuestDocument.id: guest_id}}),
            session=session,
        )

    async def remove_guest_from_event(
        self,
        event_id: PydanticObjectId,
        guest_id: PydanticObjectId,
        session: Optional[AsyncIOMotorClientSession] = None,
    ) -> UpdateResult:
        res = await EventDocument.find_one(EventDocument.id == event_id).update_one(
            Pull({EventDocument.guests: {GuestDocument.id: guest_id}}), session=session
        )

        if not res.matched_count:
            raise EventNotFound(f"Event with id {event_id} not found")

        return res

    async def find_guests_by_event_id(
        self, event_id: PydanticObjectId
    ) -> EventOnlyWithGuests:
        event = await EventDocument.find_one(
            EventDocument.id == event_id, projection_model=EventOnlyWithGuests
        )
        if not event:
            raise EventNotFound(f"Event with id {event_id} not found")

        return event

    async def add_guest_to_event(
        self,
        event_id: PydanticObjectId,
        guest_basic_info: BasicRegistrationInfo,
        session: Optional[AsyncIOMotorClientSession] = None,
    ) -> UpdateResult:
        res = await EventDocument.find_one(EventDocument.id == event_id).update_one(
            AddToSet({EventDocument.guests: guest_basic_info}), session=session
        )

        if not res.matched_count:
            raise EventNotFound(f"Event with id {event_id} not found")

        return res

    async def add_organizer_to_event(
        self,
        event_id: PydanticObjectId,
        organizer_id: PydanticObjectId,
        session: Optional[AsyncIOMotorClientSession] = None,
    ) -> UpdateResult:
        res = await EventDocument.find_one(EventDocument.id == event_id).update_one(
            AddToSet({EventDocument.organizers: organizer_id}), session=session
        )

        if not res.matched_count:
            raise EventNotFound(f"Event with id {event_id} not found")

        return res

    async def remove_organizer_from_all_events(
        self,
        organizer_id: PydanticObjectId,
        session: Optional[AsyncIOMotorClientSession] = None,
    ) -> UpdateResult:
        return await EventDocument.find_many(
            EventDocument.organizers == organizer_id
        ).update_many(Pull({EventDocument.organizers: organizer_id}), session=session)

    async def find_events_by_organizer_id(
        self, organizer_id: PydanticObjectId
    ) -> list[EventDocument]:
        return await EventDocument.find_many(
            EventDocument.organizers == organizer_id,
        ).to_list()


def get_event_repository() -> EventRepository:
    return EventRepository()


CommonEventRepository = Annotated[EventRepository, Depends(get_event_repository)]
