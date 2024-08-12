from fastapi import APIRouter, HTTPException, status

from app.api.errors.guest_not_vip import GuestNotVipException
from app.api.models.register_model import Registration, UnRegistraion
from app.api.services.register_service import CommonRegisterService


router = APIRouter()


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

            if not res.matched_count:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Not found"
                )

    except GuestNotVipException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))


@router.delete("", name="Unregister a guest from an event - Deletes a connection")
async def unregister(
    unregister: UnRegistraion, register_service: CommonRegisterService
):
    registration_result = await register_service.unregister(unregister)

    for res in registration_result:
        if not res.acknowledged:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to register",
            )

        if not res.matched_count:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Not found"
            )
