# event_service.py
from typing import Annotated

from beanie import PydanticObjectId
from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClientSession
from pymongo.results import UpdateResult

from app.api.models.event_model import Event, PartialEvent
from app.api.models.register_model import BasicRegistrationInfo
from app.api.repositories.event_repository import CommonEventRepository, EventRepository


class EventService:
    _event_repository: EventRepository

    def __init__(self, event_repo: EventRepository) -> None:
        self._event_repository = event_repo

    async def get_all(self):
        return await self._event_repository.find_all()

    async def get_one_by_id(self, id: PydanticObjectId):
        return await self._event_repository.find_one_by_id(id)

    async def create(self, event: Event):
        return await self._event_repository.create(event)

    async def update_one_by_id(self, id: PydanticObjectId, event: PartialEvent):
        return await self._event_repository.update_one_by_id(id, event)

    async def delete_one_by_id(
        self,
        id: PydanticObjectId,
        session: AsyncIOMotorClientSession | None = None,
    ):
        return await self._event_repository.delete_one_by_id(id, session=session)

    async def remove_guest_from_all_events(
        self,
        guest_id: PydanticObjectId,
        session: AsyncIOMotorClientSession | None = None,
    ):
        return await self._event_repository.remove_guest_from_all_events(
            guest_id, session=session
        )

    async def remove_guest_from_event(
        self,
        event_id: PydanticObjectId,
        guest_id: PydanticObjectId,
        session: AsyncIOMotorClientSession | None = None,
    ) -> UpdateResult:
        return await self._event_repository.remove_guest_from_event(
            event_id, guest_id, session=session
        )

    async def get_guests_by_event_id(self, event_id: PydanticObjectId):
        return await self._event_repository.find_guests_by_event_id(event_id)

    async def add_guest_to_event(
        self,
        event_id: PydanticObjectId,
        guest_basic_info: BasicRegistrationInfo,
        session: AsyncIOMotorClientSession | None = None,
    ) -> UpdateResult:
        return await self._event_repository.add_guest_to_event(
            event_id, guest_basic_info, session=session
        )


def get_event_service(event_repo: CommonEventRepository):
    return EventService(event_repo)


CommonEventService = Annotated[EventService, Depends(get_event_service, use_cache=True)]
