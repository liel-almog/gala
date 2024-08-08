from __future__ import annotations

# dependency_injection.py
from typing import Annotated

from fastapi import Depends

from src.api.services.event_service import EventService
from src.api.services.guest_service import GuestService


def get_event_service(guest_service: "GuestService"):
    from src.api.services.event_service import (
        EventService,
    )  # Dynamic import to avoid circular dependency

    return EventService(guest_service)


CommonEventService = Annotated[
    "EventService",
    Depends(lambda: get_event_service(Depends("CommonGuestService")), use_cache=True),
]


def get_guest_service(event_service: "EventService"):
    from src.api.services.guest_service import (
        GuestService,
    )  # Dynamic import to avoid circular dependency

    return GuestService(event_service)


CommonGuestService = Annotated[
    "GuestService",
    Depends(lambda: get_guest_service(Depends("CommonEventService")), use_cache=True),
]
