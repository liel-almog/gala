import logging
from typing import Annotated
from beanie import PydanticObjectId
from fastapi import APIRouter, Body, HTTPException, Path, status

from app.api.models.guest_model import GuestDocument, PartialGuestDocument
from app.api.services.guest_service import CommonGuestService
from app.api.services.register_service import CommonRegisterService


router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("", name="Get all guests", response_model=list[GuestDocument])
async def get_all(guest_service: CommonGuestService):
    try:
        guests = await guest_service.get_all()
        logger.info(f"Successfully fetched {len(guests)} guests")
        return guests
    except Exception as e:
        logger.error(f"Could not fetch all guests. Exited with {e}")
        raise e


@router.get("/{guest_id}", name="Get guest by id", response_model=GuestDocument)
async def get_guest_by_id(
    guest_id: Annotated[PydanticObjectId, Path()], guest_service: CommonGuestService
):
    try:
        guest = await guest_service.get_one_by_id(guest_id)
        if not guest:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Guest not found"
            )

        logger.info(f"Fetched guest with id {guest_id}")

        return guest
    except Exception as e:
        logger.error(f"Could not fetch guest with id {guest_id}")
        raise e


@router.post("", name="Create guest", response_model=GuestDocument)
async def create(
    guest_to_insert: Annotated[GuestDocument, Body()], guest_service: CommonGuestService
):
    try:
        created_guest = await guest_service.create(guest_to_insert)
        logger.info(f"Created guest with id {created_guest.id}")
        return created_guest
    except Exception as e:
        logger.error("Could not create guest")
        raise e


@router.patch("/{guest_id}", name="Update guest")
async def update_one_by_id(
    guest_id: Annotated[PydanticObjectId, Path()],
    guest: Annotated[PartialGuestDocument, Body()],
    guest_service: CommonGuestService,
):
    try:
        update_result = await guest_service.update_one_by_id(guest_id, guest)
        logger.info(f"Updated guest with id {guest_id}")

        if update_result.matched_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Guest not found"
            )

        return {"id": str(guest_id)}
    except Exception as e:
        logger.error(f"Could not update guest with id {guest_id}")
        raise e


@router.delete("/{guest_id}")
async def delete(
    guest_id: Annotated[PydanticObjectId, Path()],
    register_service: CommonRegisterService,
):
    return await register_service.delete_guest(guest_id)


@router.get("/{guest_id}/events")
async def get_events_by_guest_id(
    guest_service: CommonGuestService, guest_id: Annotated[PydanticObjectId, Path()]
):
    pass
