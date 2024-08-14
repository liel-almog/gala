import logging
from typing import Annotated

from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException, Path, status

from app.api.errors.organizer_not_found import OrganizerNotFound
from app.api.models.organizer_model import Organizer, PartialOrganizer
from app.api.services.organizer_service import CommonOrganizerService

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("")
async def get_all(organizer_service: CommonOrganizerService):
    organizers = await organizer_service.get_all()
    logger.info(f"Returning {len(organizers)} organizers")

    return organizers


@router.get("/{organizer_id}")
async def get_one_by_id(
    organizer_id: Annotated[PydanticObjectId, Path()],
    organizer_service: CommonOrganizerService,
):
    try:
        return await organizer_service.get_by_id(organizer_id)
    except OrganizerNotFound as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("")
async def create(organizer: Organizer, organizer_service: CommonOrganizerService):
    return await organizer_service.create(organizer)


@router.patch("/{organizer_id}")
async def update(
    organizer_id: PydanticObjectId,
    organizer: PartialOrganizer,
    organizer_service: CommonOrganizerService,
):
    try:
        await organizer_service.update(organizer_id, organizer)

        return {"id": str(organizer_id)}
    except OrganizerNotFound as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/{organizer_id}")
async def delete():
    pass
