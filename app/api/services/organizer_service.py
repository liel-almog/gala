from beanie import PydanticObjectId
from fastapi import Depends
from typing_extensions import Annotated

from app.api.models.organizer_model import Organizer, PartialOrganizer
from app.api.repositories.event_repository import CommonEventRepository, EventRepository
from app.api.repositories.organizer_repository import (
    CommonOrganizerRepository,
    OrganizerRepository,
)


class OrganizerService:
    _organizer_repositoy: OrganizerRepository
    _event_repository: EventRepository

    def __init__(
        self, organizer_repo: OrganizerRepository, event_repo: EventRepository
    ) -> None:
        self._organizer_repositoy = organizer_repo
        self._event_repository = event_repo

    async def get_all(self):
        return await self._organizer_repositoy.find_all()

    async def get_one_by_id(self, id: PydanticObjectId):
        return await self._organizer_repositoy.find_one_by_id(id)

    async def create(self, organizer: Organizer):
        return await self._organizer_repositoy.create(organizer)

    async def update_one_by_id(self, id: PydanticObjectId, organizer: PartialOrganizer):
        return await self._organizer_repositoy.update_one_by_id(id, organizer)

    async def get_events_by_organizer_id(self, organizer_id: PydanticObjectId):
        return await self._event_repository.find_events_by_organizer_id(organizer_id)


def get_organizer_service(
    organizer_repo: CommonOrganizerRepository, event_repo: CommonEventRepository
):
    return OrganizerService(organizer_repo, event_repo)


CommonOrganizerService = Annotated[OrganizerService, Depends(get_organizer_service)]
