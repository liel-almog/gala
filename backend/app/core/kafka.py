from typing import Annotated
from fastapi import Depends
from kafka import KafkaProducer
import json
from app.core.config import settings


class KafkaProducerWrapper:
    _producer: KafkaProducer | None = None

    @property
    def producer(self) -> KafkaProducer:
        # if self._producer is None:
        #     raise Exception("Kafka producer is not initialized")

        return self._producer

    def start_producer(self):
        self._producer = KafkaProducer(
            bootstrap_servers=settings.KAFKA_BROKERS,
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        )

    def close_producer(self):
        if self._producer is None:
            raise Exception("Kafka producer is not initialized.")

        try:
            self._producer.close()
        except Exception as _e:
            raise _e

    def get_producer(self) -> KafkaProducer:
        return self.producer


VIP_CUSTOM_REQUEST_TOPIC = "vip_custom_request"


kafka_producer_wrapper = KafkaProducerWrapper()
CommonKafkaProducer = Annotated[
    KafkaProducer, Depends(kafka_producer_wrapper.get_producer)
]
