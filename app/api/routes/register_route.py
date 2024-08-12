import logging
from fastapi import APIRouter, HTTPException, status

from app.api.errors.event_not_found import EventNotFound
from app.api.errors.guest_not_found import GuestNotFound
from app.api.errors.guest_not_vip import GuestNotVipException
from app.api.models.register_model import Registration, UnRegistraion
from app.api.services.register_service import CommonRegisterService


router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("", name="Register a guest to an event - Creates a connection")
async def registration(
    registration: Registration, register_service: CommonRegisterService
):
    try:
        registration_result = await register_service.register(registration)

        # We can send another status if we did not modify the document but I don't think it's necessary
        for res in registration_result:
            if not res.acknowledged:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to register",
                )

        logger.info(
            f"Successfully registered guest {registration.guest_id} to event {registration.event_id}"
        )

    except GuestNotVipException as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except GuestNotFound as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except EventNotFound as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("", name="Unregister a guest from an event - Deletes a connection")
async def unregister(
    unregister: UnRegistraion, register_service: CommonRegisterService
):
    try:
        registration_result = await register_service.unregister(unregister)

        for res in registration_result:
            if not res.acknowledged:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to register",
                )

        logger.info(
            f"Successfully unregistered guest {unregister.guest_id} from event {unregister.event_id}"
        )

    except GuestNotFound as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except EventNotFound as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
