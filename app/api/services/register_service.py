from asyncio import gather
from typing import Annotated
from beanie import PydanticObjectId
from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClient

from app.api.services.event_service import CommonEventService, EventService
from app.api.services.guest_service import CommonGuestService, GuestService
from app.core.db import CommonMongoClient


class RegisterService:
    _client: AsyncIOMotorClient
    _event_service: EventService
    _guest_service: GuestService

    def __init__(
        self,
        client: AsyncIOMotorClient,
        event_service: EventService,
        guest_service: GuestService,
    ) -> None:
        self._client = client
        self._event_service = event_service
        self._guest_service = guest_service

    async def delete_guest(self, guest_id: PydanticObjectId):
        async with await self._client.start_session() as session:
            async with session.start_transaction():
                delete_guest_task = self._guest_service.delete_one_by_id(guest_id)
                delete_guest_from_events_task = (
                    self._event_service.delete_guest_from_events(guest_id)
                )

                await gather(*(delete_guest_task, delete_guest_from_events_task))

    async def delete_event(self, event_id: PydanticObjectId):
        async with await self._client.start_session() as session:
            async with session.start_transaction():
                delete_event_task = self._event_service.delete_one_by_id(event_id)
                delete_event_from_guests_task = (
                    self._guest_service.delete_event_from_guests(event_id)
                )

                await gather(*(delete_event_from_guests_task, delete_event_task))

    async def register():
        pass

    async def unregister():
        pass


def get_register_service(
    client: CommonMongoClient,
    event_service: CommonEventService,
    guest_service: CommonGuestService,
):
    return RegisterService(client, event_service, guest_service)


CommonRegisterService = Annotated[RegisterService, Depends(get_register_service)]
