import logging
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from core.config import settings
from models.guest_model import GuestDocument


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
                document_models=[GuestDocument],
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
