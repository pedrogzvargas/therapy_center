import json
import uuid
from datetime import datetime
from decimal import Decimal
from confluent_kafka import Producer
from modules.shared.bus.event.domain import EventBus

class CustomJSONEncoder(json.JSONEncoder):

    def default(self, obj):

        if isinstance(obj, uuid.UUID):
            return str(obj)

        if isinstance(obj, datetime):
            return obj.isoformat()

        if isinstance(obj, Decimal):
            return float(obj)

        if isinstance(obj, set):
            return list(obj)

        return super().default(obj)

class KafkaEventBus(EventBus):

    def __init__(self, url):
        self.url = url
        self.producer = Producer(
            {"bootstrap.servers": f"{self.url}"}
        )

    def publish(self, domain_events):
        for domain_event in domain_events:
            self.producer.produce(
                topic="app",
                value=json.dumps(domain_event.to_primitives(), cls=CustomJSONEncoder).encode("utf-8")
            )

        self.producer.flush()
