import logging
from typing import Annotated
from beanie import PydanticObjectId
from fastapi import APIRouter, Body, HTTPException, Path, status

from app.api.errors.event_not_found import EventNotFound
from app.api.models.event_model import EventDocument, PartialEventDocument
from app.api.services.event_service import CommonEventService
from app.api.services.register_service import CommonRegisterService

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("", name="Get all events", response_model=list[EventDocument])
async def get_all(event_service: CommonEventService):
    try:
        events = await event_service.get_all()
        logger.info(f"Successfully fetched {len(events)} events")
        return events
    except Exception as e:
        logger.error("Error while fetching all events")
        raise e


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

    except Exception as e:
        logger.error(f"Error while fetching event with id {event_id}")
        raise e


@router.post("", name="Create event", response_model=EventDocument)
async def create(
    event_to_insert: Annotated[EventDocument, Body()], event_service: CommonEventService
):
    created_event = await event_service.create(event_to_insert)
    logger.info(f"Created event with id {created_event.id}")

    return created_event


@router.patch("/{event_id}", name="Update event")
async def update_one_by_id(
    event_id: Annotated[PydanticObjectId, Path()],
    event: Annotated[PartialEventDocument, Body()],
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

    except EventNotFound as _e:
        logger.error(f"Event with id {event_id} not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Event not found"
        )

    except Exception as e:
        logger.error(f"Could not update event with id {event_id}")
        raise e


@router.delete("/{event_id}", name="Delete event")
async def delete(
    event_id: Annotated[PydanticObjectId, Path()],
    register_service: CommonRegisterService,
):
    try:
        [del_res] = await register_service.delete_event(event_id)

        if not del_res.acknowledged:
            logger.error(f"Could not delete event with id {event_id}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Could not delete event",
            )
    except EventNotFound as _e:
        logger.error(f"Event with id {event_id} not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Event not found"
        )


@router.get("/{event_id}/guests")
async def get_guests_by_event_id():
    pass
