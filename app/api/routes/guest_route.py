from fastapi import APIRouter


router = APIRouter()


@router.get("")
async def get_all():
    pass


@router.get("/{guest_id}")
async def get_guest_by_id():
    pass


@router.post("")
async def create():
    pass


@router.patch("/{guest_id}")
async def update():
    pass


@router.delete("/{guest_id}")
async def delete():
    pass


@router.get("/{guest_id}/events")
async def get_events_by_guest_id():
    pass
