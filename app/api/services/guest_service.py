# guest_service.py
from typing import Annotated

from fastapi import Depends
from app.api.models.event_model import Guest


class GuestService:
    def __init__(self) -> None:
        pass

    async def get_all(self):
        return await Guest.find_all().to_list()


def get_guest_service():
    return GuestService()


CommonGuestService = Annotated[GuestService, Depends(get_guest_service, use_cache=True)]
