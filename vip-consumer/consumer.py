import time
from kafka import KafkaConsumer
from kafka.errors import KafkaError
from kafka.consumer.fetcher import ConsumerRecord
from config import settings

MIN_COMMIT_COUNT = 10
TOPICS = ["vip_custom_request"]
CONSUMER_GROUP = "vip_custom_requests_group"

running = True


def msg_process(msg: ConsumerRecord):
    time.sleep(3)
    print(f"Process message: {msg.key}: {msg.value}")


def consume_loop(consumer: KafkaConsumer):
    msg_count = 0
    try:
        while running:
            # the msg is a ConsumerRecord object as defined in kafka-python docs
            # https://github.com/wbarnha/kafka-python-ng?tab=readme-ov-file#kafkaconsumer
            for msg in consumer:
                msg_process(msg)
                msg_count += 1
                if msg_count % MIN_COMMIT_COUNT == 0:
                    consumer.commit()

    except KafkaError as e:
        print(f"KafkaError: {e}")
    finally:
        # Close down consumer to commit final offsets.
        consumer.close()


def main():
    consumer = KafkaConsumer(
        *TOPICS,
        bootstrap_servers=settings.KAFKA_BROKERS,
        group_id=CONSUMER_GROUP,
        auto_offset_reset="earliest",
    )

    consume_loop(consumer)


if __name__ == "__main__":
    main()
