from fastapi import APIRouter


router = APIRouter()


@router.get("/")
async def get_all():
    pass


@router.post("/")
async def create():
    pass


@router.delete("/")
async def delete():
    pass
