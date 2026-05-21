import json
from confluent_kafka import Consumer
from modules.shared.bus.event.application import Dispatcher
from modules.shared.bus.event.application import load_subscribers

load_subscribers()

consumer = Consumer(
    {
        "bootstrap.servers": "localhost:9092",
        "group.id": "therapy-center-workers",
        "auto.offset.reset": "earliest"
    }
)

consumer.subscribe(
    [
        "app",
    ]
)

if __name__ == "__main__":

    while True:
        message = consumer.poll(1.0)

        if message is None:
            continue

        if message.error():
            print(message.error())

        try:
            event = json.loads(
                message.value().decode("utf-8")
            )

            Dispatcher.dispatch(event=event)

        except Exception as e:
            print("Kafka worker error: ", e)
