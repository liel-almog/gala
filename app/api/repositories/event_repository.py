from typing import Annotated

from beanie import PydanticObjectId, UpdateResponse
from beanie.operators import Set
from fastapi import Depends
from pymongo.results import UpdateResult

from app.api.errors.event_not_found import EventNotFound
from app.api.models.event_model import Event


class EventRepository:
    async def find_all(self):
        return await Event.find_all().to_list()

    async def find_one_by_id(self, id: PydanticObjectId):
        event = await Event.get(id)
        if not event:
            raise EventNotFound(f"Event with id {id} not found")

        return event

    async def create(self, event: Event):
        event_to_create = Event(**event.model_dump())
        return await Event.insert_one(event_to_create)

    async def update_one_by_id(
        self, id: PydanticObjectId, event: Event
    ) -> UpdateResult:
        event_dict = event.model_dump(exclude_unset=True, by_alias=True)
        res = await Event.find_one(Event.id == id).update_one(
            Set(event_dict), response_type=UpdateResponse.UPDATE_RESULT
        )

        if not res.matched_count:
            raise EventNotFound(f"Event with id {id} not found")

        return res


def get_event_repository() -> EventRepository:
    return EventRepository()


CommonEventRepository = Annotated[EventRepository, Depends(get_event_repository)]
