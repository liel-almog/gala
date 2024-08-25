import sys
from confluent_kafka import Consumer, KafkaError, KafkaException

MIN_COMMIT_COUNT = 10
TOPICS = ["vip_custom_request"]

running = True


def msg_process(msg):
    print("Received message: {}".format(msg.value().decode("utf-8")))


def consume_loop(consumer: Consumer, topics):
    try:
        consumer.subscribe(topics)

        msg_count = 0
        while running:
            msg = consumer.poll(timeout=1.0)
            if msg is None:
                continue

            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition event
                    sys.stderr.write(
                        "%% %s [%d] reached end at offset %d\n"
                        % (msg.topic(), msg.partition(), msg.offset())
                    )
                elif msg.error():
                    raise KafkaException(msg.error())
            else:
                msg_process(msg)
                msg_count += 1
                if msg_count % MIN_COMMIT_COUNT == 0:
                    consumer.commit(asynchronous=False)
    finally:
        # Close down consumer to commit final offsets.
        consumer.close()


def main():
    conf = {
        "bootstrap.servers": "localhost:29092",
        "group.id": "vip_custom_requests_group",
        "auto.offset.reset": "smallest",
    }

    consumer = Consumer(conf)

    consume_loop(consumer, TOPICS)


if __name__ == "__main__":
    main()
