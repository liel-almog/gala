from typing import Annotated
from fastapi import Depends
from kafka import KafkaProducer
import json
from app.core.config import settings

_producer = KafkaProducer(
    bootstrap_servers=settings.KAFKA_BROKERS,
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)

VIP_CUSTOM_REQUEST_TOPIC = "vip_custom_request"


def get_producer():
    return _producer


CommonKaftaProducer = Annotated[KafkaProducer, Depends(get_producer)]
