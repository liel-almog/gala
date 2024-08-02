from fastapi import APIRouter
from .event_route import router as event_router
from .guest_route import router as guest_router


api_router = APIRouter()
api_router.include_router(router=event_router, prefix="/event")
api_router.include_router(router=guest_router, prefix="/guest")
