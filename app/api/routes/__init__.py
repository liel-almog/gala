from fastapi import APIRouter
from .event_route import router as event_router
from .guest_route import router as guest_router
from .organizer_route import router as organizer_router
from .register_route import router as register_router

api_router = APIRouter()

api_router.include_router(router=event_router, prefix="/events")
api_router.include_router(router=guest_router, prefix="/guests")
api_router.include_router(router=organizer_router, prefix="/organizers")
api_router.include_router(router=register_router, prefix="/registers")
