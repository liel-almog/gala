from consumer import start_consumer
from db import start_async_mongo
from log import setup_logger


async def main():
    setup_logger()
    await start_async_mongo()
    await start_consumer()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
