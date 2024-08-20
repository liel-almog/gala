from typing import Annotated

from beanie import PydanticObjectId, UpdateResponse
from beanie.operators import Set
from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClientSession
from pymongo.results import UpdateResult

from app.api.errors.organizer_not_found import OrganizerNotFound
from app.api.models.organizer_model import (
    Organizer,
    OrganizerDocument,
    PartialOrganizer,
)


class OrganizerRepository:
    async def find_all(self):
        return await OrganizerDocument.find_all().to_list()

    async def find_one_by_id(self, id: PydanticObjectId):
        organizer = await OrganizerDocument.get(id)
        if not organizer:
            raise OrganizerNotFound(f"Organizer with id {id} not found")

        return organizer

    async def create(self, organizer: Organizer):
        organizer_to_insert = OrganizerDocument(**organizer.model_dump())
        return await organizer_to_insert.save()

    async def update_one_by_id(
        self, id: PydanticObjectId, organizer: PartialOrganizer
    ) -> UpdateResult:
        organizer_dict = organizer.model_dump(exclude_unset=True, by_alias=True)
        res = await OrganizerDocument.find_one(OrganizerDocument.id == id).update_one(
            Set(organizer_dict), response_type=UpdateResponse.UPDATE_RESULT
        )

        if not res.matched_count:
            raise OrganizerNotFound(f"Organizer with id {id} not found")

        return res

    async def delete_one_by_id(
        self, id: PydanticObjectId, session: AsyncIOMotorClientSession
    ):
        res = await OrganizerDocument.find_one(OrganizerDocument.id == id).delete_one(
            session=session
        )

        if not res.deleted_count:
            raise OrganizerNotFound(f"Organizer with id {id} not found")

        return res


def get_organizer_repository():
    return OrganizerRepository()


CommonOrganizerRepository = Annotated[
    OrganizerRepository, Depends(get_organizer_repository)
]
