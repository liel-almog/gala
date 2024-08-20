# guest_service.py
from typing import Annotated, Optional

from beanie import PydanticObjectId
from beanie.operators import Set
from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClientSession, AsyncIOMotorClient
from pymongo.results import UpdateResult

from app.api.models.event_model import EventDocument
from app.api.models.guest_model import (
    Guest,
    GuestDocument,
    PartialGuest,
)
from app.api.models.register_model import BasicRegistrationInfo
from app.api.repositories.event_repository import CommonEventRepository, EventRepository
from app.api.repositories.guest_repository import CommonGuestRepository, GuestRepository
from app.core.db import CommonMongoClient


class GuestService:
    _guest_repository: GuestRepository
    _event_repository: EventRepository
    _client: AsyncIOMotorClient

    def __init__(
        self,
        client: AsyncIOMotorClient,
        guest_repo: GuestRepository,
        event_repo: EventRepository,
    ) -> None:
        self._guest_repository = guest_repo
        self._event_repository = event_repo
        self._client = client

    async def get_all(self):
        return await self._guest_repository.find_all()

    async def get_one_by_id(self, id: PydanticObjectId):
        return await self._guest_repository.find_one_by_id(id)

    async def create(self, guest: Guest):
        return await self._guest_repository.create(guest)

    async def update_event_name_by_id(
        self, event_id: PydanticObjectId, name: str
    ) -> UpdateResult:
        return await GuestDocument.find_many({"events._id": event_id}).update_many(
            Set({f"{GuestDocument.events}.$.{EventDocument.name}": name})
        )

    async def update_one_by_id(
        self, id: PydanticObjectId, guest: PartialGuest
    ) -> UpdateResult:
        return await self._guest_repository.update_one_by_id(id, guest)

    async def delete_one_by_id(self, id: PydanticObjectId):
        async with await self._client.start_session() as session:
            async with session.start_transaction():
                delete_guest = await self._guest_repository.delete_one_by_id(
                    id, session=session
                )
                remove_guest_from_events = (
                    await self._event_repository.remove_guest_from_all_events(
                        id, session=session
                    )
                )

                return (delete_guest, remove_guest_from_events)

    async def remove_event_from_all_guests(
        self,
        event_id: PydanticObjectId,
        session: Optional[AsyncIOMotorClientSession] = None,
    ) -> UpdateResult:
        return await self._guest_repository.remove_event_from_all_guests(
            event_id, session=session
        )

    async def remove_event_from_guest(
        self,
        guest_id: PydanticObjectId,
        event_id: PydanticObjectId,
        session: Optional[AsyncIOMotorClientSession] = None,
    ) -> UpdateResult:
        return await self._guest_repository.remove_event_from_guest(
            guest_id, event_id, session=session
        )

    async def get_events_by_guest_id(self, id: PydanticObjectId):
        return await self._guest_repository.find_guest_events_by_id(id)

    async def add_event_to_guest(
        self,
        guest_id: PydanticObjectId,
        event_basic_info: BasicRegistrationInfo,
        session: Optional[AsyncIOMotorClientSession] = None,
    ) -> UpdateResult:
        self._guest_repository.add_event_to_guest(
            guest_id, event_basic_info, session=session
        )


def get_guest_service(
    guest_repository: CommonGuestRepository,
    event_repository: CommonEventRepository,
    client: CommonMongoClient,
):
    return GuestService(client, guest_repository, event_repository)


CommonGuestService = Annotated[GuestService, Depends(get_guest_service, use_cache=True)]
