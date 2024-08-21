import logging
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from config import settings
from guest_model import GuestDocument

logger = logging.getLogger(__name__)
_client: AsyncIOMotorClient | None = None


def get_mongo_client():
    global _client

    if not _client:
        raise Exception()

    return _client


async def start_async_mongo():
    global _client

    try:
        _client = AsyncIOMotorClient(settings.CONNECTION_STRING)
        await init_beanie(_client[settings.DB_NAME], document_models=[GuestDocument])
        logger.info("Connected to mongoDB")

    except Exception as _e:
        logger.error("Unable to connect to mongoDB")
        print("Error")


async def close_mongo():
    global _client

    try:
        _client.close()
        logger.info("Closed connection to mongoDB")
    except Exception as _e:
        logger.error("Unable to closed connection to mongoDB")
