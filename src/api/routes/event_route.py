from fastapi import APIRouter


router = APIRouter()


@router.get("/")
async def get_all():
    return "asd"


@router.post("/")
async def create():
    return "asd"


@router.delete("/")
async def delete():
    pass
