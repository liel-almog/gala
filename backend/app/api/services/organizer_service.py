from asyncio import gather

from beanie import PydanticObjectId
from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.results import UpdateResult, DeleteResult
from typing_extensions import Annotated

from app.api.models.event_model import EventDocument
from app.api.models.organizer_model import (
    Organizer,
    OrganizerDocument,
    PartialOrganizer,
)
from app.api.repositories.event_repository import CommonEventRepository, EventRepository
from app.api.repositories.organizer_repository import (
    CommonOrganizerRepository,
    OrganizerRepository,
)
from app.core.db import CommonMongoClient


class OrganizerService:
    _organizer_repositoy: OrganizerRepository
    _event_repository: EventRepository
    _client: AsyncIOMotorClient

    def __init__(
        self,
        client: AsyncIOMotorClient,
        organizer_repo: OrganizerRepository,
        event_repo: EventRepository,
    ) -> None:
        self._client = client
        self._organizer_repositoy = organizer_repo
        self._event_repository = event_repo

    async def get_all(self) -> list[OrganizerDocument]:
        return await self._organizer_repositoy.find_all()

    async def get_one_by_id(self, id: PydanticObjectId) -> OrganizerDocument:
        return await self._organizer_repositoy.find_one_by_id(id)

    async def create(self, organizer: Organizer) -> OrganizerDocument:
        return await self._organizer_repositoy.create(organizer)

    async def update_one_by_id(
        self, id: PydanticObjectId, organizer: PartialOrganizer
    ) -> UpdateResult:
        return await self._organizer_repositoy.update_one_by_id(id, organizer)

    async def get_events_by_organizer_id(
        self, organizer_id: PydanticObjectId
    ) -> list[EventDocument]:
        return await self._event_repository.find_events_by_organizer_id(organizer_id)

    async def delete_one_by_id(
        self, id: PydanticObjectId
    ) -> tuple[DeleteResult, UpdateResult]:
        async with await self._client.start_session() as session:
            async with session.start_transaction():
                delete_organizer_task = self._organizer_repositoy.delete_one_by_id(
                    id, session=session
                )
                remove_organizer_from_all_events_task = (
                    self._event_repository.remove_organizer_from_all_events(
                        id, session=session
                    )
                )

                return await gather(
                    *(delete_organizer_task, remove_organizer_from_all_events_task)
                )


def get_organizer_service(
    client: CommonMongoClient,
    organizer_repo: CommonOrganizerRepository,
    event_repo: CommonEventRepository,
):
    return OrganizerService(client, organizer_repo, event_repo)


CommonOrganizerService = Annotated[OrganizerService, Depends(get_organizer_service)]
