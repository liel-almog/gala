import logging
from typing import Annotated
from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException, Path, status

from app.api.errors.organizer_not_found import OrganizerNotFound
from app.api.models.organizer_model import (
    Organizer,
    OrganizerDocument,
    PartialOrganizer,
)
from app.api.services.organizer_service import CommonOrganizerService


router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("", name="Get all organizers", response_model=list[OrganizerDocument])
async def get_all(organizer_service: CommonOrganizerService):
    organizers = await organizer_service.get_all()
    logger.info(f"Successfully fetched {len(organizers)} organizers")

    return organizers


@router.get(
    "/{organizer_id}", name="Get organizer by id", response_model=OrganizerDocument
)
async def get_one_by_id(
    organizer_id: Annotated[PydanticObjectId, Path()],
    organizer_service: CommonOrganizerService,
):
    try:
        organizer = await organizer_service.get_one_by_id(organizer_id)
        logger.info(f"Fetch organizer with id {organizer_id}")

        return organizer
    except OrganizerNotFound as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("", name="Create organizer", response_model=OrganizerDocument)
async def create(organizer: Organizer, organizer_service: CommonOrganizerService):
    organizer = await organizer_service.create(organizer)
    logger.info(f"Created organizer with id {organizer.id}")

    return organizer


@router.patch("/{organizer_id}", name="Update organizer")
async def update(
    organizer_id: Annotated[PydanticObjectId, Path()],
    organizer: PartialOrganizer,
    organizer_service: CommonOrganizerService,
):
    try:
        await organizer_service.update_one_by_id(organizer_id, organizer)
        logger.info(f"Updated organizer with id {organizer_id}")

        return {"id": str(organizer_id)}
    except OrganizerNotFound as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/{organizer_id}/events", name="Get events by organizer id")
async def get_events_by_organizer_id(
    organizer_id: Annotated[PydanticObjectId, Path()],
    organizer_service: CommonOrganizerService,
):
    events = await organizer_service.get_events_by_organizer_id(organizer_id)
    logger.info(f"Fetch {len(events)} events by organizer id {organizer_id}")

    return events


@router.delete("/{organizer_id}")
async def delete():
    pass
