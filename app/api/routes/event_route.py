import logging
from typing import Annotated
from beanie import PydanticObjectId
from fastapi import APIRouter, Body, HTTPException, Path, status

from app.api.errors.event_not_found import EventNotFound
from app.api.models.event_model import (
    Event,
    EventDocument,
    EventOnlyWithGuests,
    PartialEvent,
)
from app.api.services.event_service import CommonEventService

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("", name="Get all events", response_model=list[EventDocument])
async def get_all(event_service: CommonEventService):
    events = await event_service.get_all()
    logger.info(f"Successfully fetched {len(events)} events")

    return events


@router.get("/{event_id}", name="Get event by id", response_model=EventDocument)
async def get_event_by_id(
    event_id: Annotated[PydanticObjectId, Path()], event_service: CommonEventService
):
    try:
        event = await event_service.get_one_by_id(event_id)
        logger.info(f"Fetched event with id {event_id}")

        return event
    except EventNotFound as _e:
        logger.error(f"Event with id {event_id} not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Event not found"
        )


@router.post("", name="Create event", response_model=EventDocument)
async def create(
    event_to_insert: Annotated[Event, Body()], event_service: CommonEventService
):
    created_event = await event_service.create(event_to_insert)
    logger.info(f"Created event with id {created_event.id}")

    return created_event


@router.patch("/{event_id}", name="Update event")
async def update_one_by_id(
    event_id: Annotated[PydanticObjectId, Path()],
    event: Annotated[PartialEvent, Body()],
    event_service: CommonEventService,
):
    try:
        update_result = await event_service.update_one_by_id(event_id, event)
        logger.info(f"Updated event with id {event_id}")

        if not update_result.acknowledged:
            logger.error(f"Error while updating event with id {event_id}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unable to update",
            )

        return {"id": str(event_id)}
    except EventNotFound as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/{event_id}", name="Delete event")
async def delete(
    event_id: Annotated[PydanticObjectId, Path()],
    event_service: CommonEventService,
):
    try:
        await event_service.delete_one_by_id(event_id)

        return {"id": str(event_id)}
    except EventNotFound as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get(
    "/{event_id}/guests",
    response_model=EventOnlyWithGuests,
    name="Get guests by event id",
)
async def get_guests_by_event_id(
    event_id: Annotated[PydanticObjectId, Path()], event_service: CommonEventService
):
    try:
        return await event_service.get_guests_by_event_id(event_id)
    except EventNotFound as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
