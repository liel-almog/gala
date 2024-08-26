from core.consumer import start_consumer
from core.db import mongo_client_manager
from core.log import setup_logger


async def main():
    setup_logger()
    await mongo_client_manager.start_async_mongo()
    await start_consumer()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
