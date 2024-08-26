import logging
from typing import Annotated
from beanie import init_beanie
from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClient

from app.api.models.event_model import EventDocument
from app.api.models.guest_model import GuestDocument
from app.api.models.organizer_model import OrganizerDocument
from app.core.config import settings


logger = logging.getLogger(__name__)


class MongoDBClientManager:
    _client: AsyncIOMotorClient | None = None

    @property
    def mongo_client(self) -> AsyncIOMotorClient:
        return self._client

    async def start_async_mongo(self):
        try:
            self._client = AsyncIOMotorClient(settings.CONNECTION_STRING)
            await init_beanie(
                self._client[settings.DB_NAME],
                document_models=[EventDocument, GuestDocument, OrganizerDocument],
            )
            logger.info("Connected to mongoDB")

        except Exception as _e:
            logger.error("Unable to connect to mongoDB")
            print("Error")

    async def close_mongo(self):
        if self._client is None:
            raise Exception("MongoDB client is not initialized.")

        try:
            self._client.close()
            logger.info("Closed connection to MongoDB")
        except Exception as _e:
            logger.error("Unable to close connection to MongoDB")
            raise _e

    def get_mongo_client(self) -> AsyncIOMotorClient:
        return self.mongo_client


mongo_client_manager = MongoDBClientManager()
CommonMongoClient = Annotated[
    AsyncIOMotorClient, Depends(mongo_client_manager.get_mongo_client, use_cache=True)
]
