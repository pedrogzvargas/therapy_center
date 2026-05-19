import os
from kombu import Exchange
from kombu import Producer
from kombu import Queue
from kombu import Connection
from modules.shared.bus.event.domain import EventBus


class RabbitEventBus(EventBus):
    """
    RabbitMQ event bus creator
    """

    def __init__(
        self,
        url: str = None,
        exchange_name: str = None,
        exchange_type: str = None,
        queue_name: str = None,
        routing_key: str = None
    ):
        """
        Args:
            url: RabbitMQ server ulr
            exchange_name: RabbitMQ exchange name
            exchange_type: RabbitMQ exchange type
            queue_name: RabbitMQ queue name
            routing_key: RabbitMQ routing key
        """

        url = url or os.getenv('RABBITMQ_URL')
        exchange_name = exchange_name or os.getenv('RABBITMQ_EXCHANGE_NAME')
        exchange_type = exchange_type or os.getenv('RABBITMQ_EXCHANGE_TYPE')
        queue_name = queue_name or os.getenv('RABBITMQ_QUEUE_NAME')
        routing_key = routing_key or os.getenv('RABBITMQ_ROUTING_KEY')

        self.__connection = Connection(url)
        self.__channel = self.__connection.channel()
        self.__exchange = Exchange(name=exchange_name, type=exchange_type)
        self.__producer = Producer(
            exchange=self.__exchange,
            channel=self.__channel,
            routing_key=routing_key,
            serializer="json",
        )
        self.__queue = Queue(name=queue_name, exchange=self.__exchange, routing_key=routing_key)
        self.__queue.maybe_bind(self.__connection)
        self.__queue.declare()

    def publish(self, domain_events):
        """function to publish on RabbitMQ"""
        # if not isinstance(message, dict):
        #    raise ValueError(f"{message} is no instance of dict")
        # json_message = json.dumps(message)
        self.__producer.publish(domain_events)
