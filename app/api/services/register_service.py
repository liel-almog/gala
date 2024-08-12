from asyncio import gather
from typing import Annotated

from beanie import PydanticObjectId
from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClient

from app.api.errors.event_not_found import EventNotFound
from app.api.errors.guest_not_found import GuestNotFound
from app.api.errors.guest_not_vip import GuestNotVipException
from app.api.models.register_model import (
    BasicRegistrationInfo,
    Registration,
    UnRegistraion,
)
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
        event = await self._event_service.get_one_by_id(registration.event_id)
        if not event:
            raise EventNotFound("Event not found")

        # No need to fetch the guest if the event is not VIP
        if event.is_vip_event:
            guest = await self._guest_service.get_one_by_id(registration.guest_id)
            if not guest:
                raise GuestNotFound("Guest not found")

            if event.is_vip_event and not guest.is_vip:
                raise GuestNotVipException("Guest is not VIP")

        async with await self._client.start_session() as session:
            async with session.start_transaction():
                basic_event = BasicRegistrationInfo(id=event.id, name=event.name)
                basic_guest = BasicRegistrationInfo(id=guest.id, name=guest.name)

                add_event_to_guest_task = self._guest_service.add_event_to_guest(
                    guest_id=registration.guest_id, event_basic_info=basic_event
                )
                add_guest_to_event_task = self._event_service.add_guest_to_event(
                    event_id=registration.event_id, guest_basic_info=basic_guest
                )

                return await gather(*(add_event_to_guest_task, add_guest_to_event_task))

    async def unregister(self, unregister: UnRegistraion):
        async with await self._client.start_session() as session:
            async with session.start_transaction():
                remove_event_from_guest = await (
                    self._guest_service.remove_event_from_guest(
                        guest_id=unregister.guest_id, event_id=unregister.event_id
                    )
                )

                if not remove_event_from_guest.matched_count:
                    raise GuestNotFound("Guest not found")

                remove_guest_from_event = await (
                    self._event_service.remove_guest_from_event(
                        event_id=unregister.event_id, guest_id=unregister.guest_id
                    )
                )

                if not remove_guest_from_event.matched_count:
                    raise EventNotFound("Event not found")

                return (remove_event_from_guest, remove_guest_from_event)


def get_register_service(
    client: CommonMongoClient,
    event_service: CommonEventService,
    guest_service: CommonGuestService,
):
    return RegisterService(client, event_service, guest_service)


CommonRegisterService = Annotated[RegisterService, Depends(get_register_service)]
