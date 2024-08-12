from asyncio import gather
from typing import Annotated

from beanie import PydanticObjectId
from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClient

from app.api.models.register_model import Registration, UnRegistraion
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
                remove_guest_task = self._guest_service.delete_one_by_id(guest_id)
                remove_guest_from_events_task = (
                    self._event_service.remove_guest_from_all_events(guest_id)
                )

                return await gather(*(remove_guest_task, remove_guest_from_events_task))

    async def delete_event(self, event_id: PydanticObjectId):
        async with await self._client.start_session() as session:
            async with session.start_transaction():
                delete_event_task = self._event_service.delete_one_by_id(event_id)
                delete_event_from_guests_task = (
                    self._guest_service.remove_event_from_all_guests(event_id)
                )

                return await gather(*(delete_event_from_guests_task, delete_event_task))

    async def register(self, registration: Registration):
        async with await self._client.start_session() as session:
            async with session.start_transaction():
                add_event_to_guest_task = self._guest_service.add_event_to_guest(
                    guest_id=registration.guest.id, event=registration.event
                )
                add_guest_to_event_task = self._event_service.add_guest_to_event(
                    event_id=registration.event.id, guest=registration.guest
                )

                return await gather(*(add_event_to_guest_task, add_guest_to_event_task))

    async def unregister(self, unregister: UnRegistraion):
        async with await self._client.start_session() as session:
            async with session.start_transaction():
                delete_event_from_guest_task = (
                    self._guest_service.remove_event_from_guest(
                        guest_id=unregister.guest_id, event_id=unregister.event_id
                    )
                )
                delete_guest_from_event_task = (
                    self._event_service.remove_guest_from_event(
                        event_id=unregister.event_id, guest_id=unregister.guest_id
                    )
                )

                return await gather(
                    *(delete_event_from_guest_task, delete_guest_from_event_task)
                )


def get_register_service(
    client: CommonMongoClient,
    event_service: CommonEventService,
    guest_service: CommonGuestService,
):
    return RegisterService(client, event_service, guest_service)


CommonRegisterService = Annotated[RegisterService, Depends(get_register_service)]
