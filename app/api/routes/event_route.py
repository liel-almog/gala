from typing import Annotated
from fastapi import APIRouter, Body

from app.api.models.event_model import Event, EventDocument

router = APIRouter()


@router.get("")
async def get_all():
    return await EventDocument.find_all().to_list()


@router.get("/{event_id}")
async def get_event_by_id():
    pass


@router.post("")
async def create(event: Annotated[Event, Body()]):
    print(event)


@router.patch("/{event_id}")
async def update():
    pass


@router.delete("/{event_id}")
async def delete():
    pass


@router.get("/{event_id}/guests")
async def get_guests_by_event_id():
    pass
