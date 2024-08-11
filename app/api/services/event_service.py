# event_service.py
from typing import Annotated

from beanie import PydanticObjectId, UpdateResponse
from beanie.operators import Set
from fastapi import Depends
from pymongo.results import UpdateResult

from app.api.models.event_model import EventDocument


class EventService:
    def __init__(self) -> None:
        pass

    async def get_all(self):
        return await EventDocument.find_all().to_list()

    async def get_one_by_id(self, id: PydanticObjectId):
        return await EventDocument.find_one(EventDocument.id == id)

    async def create(self, event: EventDocument):
        return await EventDocument.insert_one(event)

    async def update_one_by_id(
        self, id: PydanticObjectId, event: EventDocument
    ) -> UpdateResult:
        event_dict = event.model_dump(exclude_unset=True, by_alias=True)
        return await EventDocument.find_one(EventDocument.id == id).update_one(
            Set(event_dict), response_type=UpdateResponse.UPDATE_RESULT
        )


def get_event_service():
    return EventService()


CommonEventService = Annotated[EventService, Depends(get_event_service, use_cache=True)]
