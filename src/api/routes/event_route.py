from fastapi import APIRouter

from src.api.services.event_service import CommonEventService
from src.api.services.guest_service import CommonGuestService


router = APIRouter()


@router.get("")
async def get_all(guest_service: CommonGuestService):
    return await guest_service.get_one()


@router.post("")
async def create(event_service: CommonEventService):
    return await event_service.get_all()


# @router.delete("/")
# async def delete():
#     pass
