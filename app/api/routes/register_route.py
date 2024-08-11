from fastapi import APIRouter


router = APIRouter()


@router.post("/registration")
async def registration():
    pass


@router.delete("/unregister")
async def unregister():
    pass
