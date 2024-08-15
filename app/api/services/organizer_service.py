from typing import Annotated

from beanie import PydanticObjectId, UpdateResponse
from beanie.operators import Set
from fastapi import Depends
from pymongo.results import UpdateResult

from app.api.errors.organizer_not_found import OrganizerNotFound
from app.api.models.organizer_model import Organizer, OrganizerDocument


class OrganizerService:
    async def get_all(self):
        return await OrganizerDocument.find_all().to_list()

    async def get_by_id(self, organizer_id: PydanticObjectId):
        organizer = await OrganizerDocument.get(organizer_id)
        if not organizer:
            raise OrganizerNotFound(f"Organizer with id {organizer_id} not found")

        return organizer

    async def create(self, organizer: Organizer):
        organizer_document = OrganizerDocument(**organizer.model_dump())
        return await OrganizerDocument.insert_one(organizer_document)

    async def update(self, id: PydanticObjectId, organizer: Organizer) -> UpdateResult:
        organizer_dict = organizer.model_dump(exclude_unset=True, by_alias=True)
        res = await OrganizerDocument.find_one(OrganizerDocument.id == id).update_one(
            Set(organizer_dict), response_type=UpdateResponse.UPDATE_RESULT
        )

        if not res.matched_count:
            raise OrganizerNotFound(f"Organizer with id {id} not found")

        return res

    async def delete(self, organizer_id: PydanticObjectId):
        return await OrganizerDocument.find_one(
            OrganizerDocument.id == organizer_id
        ).delete_one()


def get_organizer_service():
    return OrganizerService()


CommonOrganizerService = Annotated[OrganizerService, Depends(get_organizer_service)]
