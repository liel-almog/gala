from fastapi import APIRouter


router = APIRouter()


@router.get("")
async def get_all():
    pass


@router.get("/{organizer_id}")
async def get_one_by_id():
    pass


@router.post("")
async def create():
    pass


@router.patch("/{organizer_id}")
async def update():
    pass


@router.delete("/{organizer_id}")
async def delete():
    pass
