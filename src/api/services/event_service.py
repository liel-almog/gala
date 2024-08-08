# event_service.py
from typing import Annotated

from fastapi import Depends
from src.api.model.event_model import Event
from src.api.services.guest_service import GuestService


class EventService:
    _guest_service: "GuestService"  # Type hint as a string to avoid direct import

    def __init__(self, guest_service: "GuestService") -> None:
        self._guest_service = guest_service

    async def get_all(self):
        return await Event.find_many({}).to_list()


def get_event_service(guest_service: "GuestService"):
    return EventService(guest_service)


CommonEventService = Annotated[
    EventService,
    Depends(lambda: get_event_service(Depends("CommonGuestService")), use_cache=True),
]
