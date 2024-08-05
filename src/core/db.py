from typing import Annotated
from beanie import init_beanie
from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClient

from src.api.model.event_model import Event
from src.core.config import settings


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
        await init_beanie(_client[settings.DB_NAME], document_models=[Event])

    except Exception as _e:
        print("Error")
