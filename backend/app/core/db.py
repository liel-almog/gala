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
_client: AsyncIOMotorClient | None = None


def get_mongo_client():
    global _client

    if not _client:
        raise Exception()

    return _client


CommonMongoClient = Annotated[
    AsyncIOMotorClient, Depends(get_mongo_client, use_cache=True)
]


async def start_async_mongo():
    global _client

    try:
        _client = AsyncIOMotorClient(settings.CONNECTION_STRING)
        await init_beanie(
            _client[settings.DB_NAME],
            document_models=[EventDocument, GuestDocument, OrganizerDocument],
        )
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
