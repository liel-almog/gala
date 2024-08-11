# event_service.py
from typing import Annotated

from fastapi import Depends
from app.api.models.event_model import Event


class EventService:
    def __init__(self) -> None:
        pass

    async def get_all(self):
        return await Event.find_many({}).to_list()


def get_event_service():
    return EventService()


CommonEventService = Annotated[EventService, Depends(get_event_service, use_cache=True)]
