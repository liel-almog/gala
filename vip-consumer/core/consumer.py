import asyncio
import json
import logging

from beanie import UpdateResponse
from beanie.operators import Set
from pymongo.results import UpdateResult
from kafka import KafkaConsumer
from kafka.consumer.fetcher import ConsumerRecord
from kafka.errors import KafkaError

from core.config import settings
from models.guest_model import CustomRequest, GuestDocument

logger = logging.getLogger(__name__)

MIN_COMMIT_COUNT = 10
TOPICS = ["vip_custom_request"]
CONSUMER_GROUP = "vip_custom_requests_group"


running = True


async def msg_process(msg: ConsumerRecord) -> UpdateResult:
    custom_request = CustomRequest(**json.loads(msg.value))
    logger.info(f"Processing custom request: {custom_request}")
    await asyncio.sleep(3)

    res = await GuestDocument.find_one(
        {"customRequests._id": custom_request.id}
    ).update_one(
        Set({"customRequests.$.fulfilled": True}),
        response_type=UpdateResponse.UPDATE_RESULT,
    )

    return res


# To use really asyncronous code with kafka we could look at https://github.com/aio-libs/aiokafka
async def consume_loop(consumer: KafkaConsumer):
    msg_count = 0
    try:
        while running:
            # the msg is a ConsumerRecord object as defined in kafka-python docs
            # https://github.com/wbarn  ha/kafka-python-ng?tab=readme-ov-file#kafkaconsumer
            for msg in consumer:
                await msg_process(msg)
                msg_count += 1
                if msg_count % MIN_COMMIT_COUNT == 0:
                    await consumer.commit_async()

    except KafkaError as e:
        print(f"KafkaError: {e}")
    finally:
        # Close down consumer to commit final offsets.
        consumer.close()


async def start_consumer():
    consumer = KafkaConsumer(
        *TOPICS,
        bootstrap_servers=settings.KAFKA_BROKERS,
        group_id=CONSUMER_GROUP,
        auto_offset_reset="earliest",
    )

    logger.info("Consumer started")

    await consume_loop(consumer)
