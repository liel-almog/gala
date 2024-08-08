# guest_service.py
from typing import Annotated

from fastapi import Depends
from src.api.model.event_model import Guest
from src.api.services.event_service import EventService


class GuestService:
    _event_service: EventService  # Type hint as a string to avoid direct import

    def __init__(self, event_service: EventService) -> None:
        self._event_service = event_service

    async def get_all(self):
        return await Guest.find_all().to_list()

    async def get_one(self):
        print("hello")
        events = await self._event_service.get_all().to_list()
        guest = await Guest.find_one()

        return {"guest": guest, "events": events}


def get_guest_service(event_service: EventService):
    return GuestService(event_service)


CommonGuestService = Annotated[
    GuestService,
    Depends(lambda: get_guest_service(Depends("CommonEventService")), use_cache=True),
]
