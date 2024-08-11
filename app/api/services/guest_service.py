# guest_service.py
from typing import Annotated

from beanie import PydanticObjectId, UpdateResponse
from beanie.operators import Set
from fastapi import Depends
from pymongo.results import UpdateResult

from app.api.models.guest_model import GuestDocument


class GuestService:
    def __init__(self) -> None:
        pass

    async def get_all(self):
        return await GuestDocument.find_all().to_list()

    async def get_one_by_id(self, id: PydanticObjectId):
        return await GuestDocument.find_one(GuestDocument.id == id)

    async def create(self, guest: GuestDocument):
        return await GuestDocument.insert_one(guest)

    async def update_one_by_id(
        self, id: PydanticObjectId, guest: GuestDocument
    ) -> UpdateResult:
        guest_dict = guest.model_dump(exclude_unset=True, by_alias=True)
        return await GuestDocument.find_one(GuestDocument.id == id).update_one(
            Set(guest_dict), response_type=UpdateResponse.UPDATE_RESULT
        )

    async def delete(self):
        pass


def get_guest_service():
    return GuestService()


CommonGuestService = Annotated[GuestService, Depends(get_guest_service, use_cache=True)]
