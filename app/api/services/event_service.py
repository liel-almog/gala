from typing import Annotated, Optional

from beanie import PydanticObjectId
from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClientSession, AsyncIOMotorClient
from pymongo.results import UpdateResult

from app.api.models.event_model import Event, PartialEvent
from app.api.models.register_model import BasicRegistrationInfo
from app.api.repositories.event_repository import CommonEventRepository, EventRepository
from app.api.repositories.guest_repository import CommonGuestRepository, GuestRepository
from app.api.repositories.organizer_repository import (
    CommonOrganizerRepository,
    OrganizerRepository,
)
from app.core.db import CommonMongoClient


class EventService:
    _event_repository: EventRepository
    _guest_repository: GuestRepository
    _organizer_repository: OrganizerRepository
    _client: AsyncIOMotorClient

    def __init__(
        self,
        client: AsyncIOMotorClient,
        event_repo: EventRepository,
        guest_repo: GuestRepository,
        organizer_repo: OrganizerRepository,
    ) -> None:
        self._client = client
        self._event_repository = event_repo
        self._guest_repository = guest_repo
        self._organizer_repository = organizer_repo

    async def get_all(self):
        return await self._event_repository.find_all()

    async def get_one_by_id(self, id: PydanticObjectId):
        return await self._event_repository.find_one_by_id(id)

    async def create(self, event: Event):
        return await self._event_repository.create(event)

    async def update_one_by_id(
        self, id: PydanticObjectId, event: PartialEvent
    ) -> UpdateResult:
        return await self._event_repository.update_one_by_id(id, event)

    async def delete_one_by_id(
        self,
        id: PydanticObjectId,
    ):
        async with await self._client.start_session() as session:
            async with session.start_transaction():
                delete_event = await self._event_repository.delete_one_by_id(
                    id, session=session
                )
                remove_event_from_all_guests = (
                    await self._guest_repository.remove_event_from_all_guests(
                        id, session=session
                    )
                )

                return (delete_event, remove_event_from_all_guests)

    async def remove_guest_from_all_events(
        self,
        guest_id: PydanticObjectId,
        session: Optional[AsyncIOMotorClientSession] = None,
    ):
        return await self._event_repository.remove_guest_from_all_events(
            guest_id, session=session
        )

    async def remove_guest_from_event(
        self,
        event_id: PydanticObjectId,
        guest_id: PydanticObjectId,
        session: Optional[AsyncIOMotorClientSession] = None,
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
        session: Optional[AsyncIOMotorClientSession] = None,
    ) -> UpdateResult:
        return await self._event_repository.add_guest_to_event(
            event_id, guest_basic_info, session=session
        )

    async def add_organizer_to_event(
        self,
        event_id: PydanticObjectId,
        organizer_id: PydanticObjectId,
        session: Optional[AsyncIOMotorClientSession] = None,
    ) -> UpdateResult:
        await self._organizer_repository.find_one_by_id(organizer_id)

        return await self._event_repository.add_organizer_to_event(
            event_id, organizer_id, session=session
        )


def get_event_service(
    client: CommonMongoClient,
    event_repo: CommonEventRepository,
    guest_repo: CommonGuestRepository,
    organizer_repo: CommonOrganizerRepository,
):
    return EventService(client, event_repo, guest_repo, organizer_repo)


CommonEventService = Annotated[EventService, Depends(get_event_service, use_cache=True)]
