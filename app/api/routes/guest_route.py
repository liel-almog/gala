import logging
from typing import Annotated
from beanie import PydanticObjectId
from fastapi import APIRouter, Body, HTTPException, Path, status

from app.api.errors.guest_not_found import GuestNotFound
from app.api.models.guest_model import (
    GuestDocument,
    GuestOnlyWithEvents,
    PartialGuestDocument,
)
from app.api.services.guest_service import CommonGuestService


router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("", name="Get all guests", response_model=list[GuestDocument])
async def get_all(guest_service: CommonGuestService):
    guests = await guest_service.get_all()
    logger.info(f"Successfully fetched {len(guests)} guests")

    return guests


@router.get("/{guest_id}", name="Get guest by id", response_model=GuestDocument)
async def get_guest_by_id(
    guest_id: Annotated[PydanticObjectId, Path()], guest_service: CommonGuestService
):
    try:
        guest = await guest_service.get_one_by_id(guest_id)
        logger.info(f"Fetched guest with id {guest_id}")

        return guest
    except GuestNotFound as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("", name="Create guest", response_model=GuestDocument)
async def create(
    guest_to_insert: Annotated[GuestDocument, Body()], guest_service: CommonGuestService
):
    created_guest = await guest_service.create(guest_to_insert)
    logger.info(f"Created guest with id {created_guest.id}")

    return created_guest


@router.patch("/{guest_id}", name="Update guest")
async def update_one_by_id(
    guest_id: Annotated[PydanticObjectId, Path()],
    guest: Annotated[PartialGuestDocument, Body()],
    guest_service: CommonGuestService,
):
    try:
        update_result = await guest_service.update_one_by_id(guest_id, guest)
        logger.info(f"Updated guest with id {guest_id}")

        if not update_result.acknowledged:
            logger.error(f"Error while fetching guest with id {guest_id}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error while updating guest with id {guest_id}",
            )

        return {"id": str(guest_id)}
    except GuestNotFound as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.delete("/{guest_id}")
async def delete(
    guest_id: Annotated[PydanticObjectId, Path()],
    guest_service: CommonGuestService,
):
    try:
        await guest_service.delete_one_by_id(guest_id)

        return {"id": str(guest_id)}
    except GuestNotFound as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get(
    "/{guest_id}/events",
    response_model=GuestOnlyWithEvents,
    name="Get events by guest id",
)
async def get_events_by_guest_id(
    guest_id: Annotated[PydanticObjectId, Path()], guest_service: CommonGuestService
):
    try:
        return await guest_service.get_events_by_guest_id(guest_id)
    except GuestNotFound as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
