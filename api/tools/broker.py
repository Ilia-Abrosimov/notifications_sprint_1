import pika
from core.config import settings


class Rabbit:
    def __init__(self, exchange_name: str, queue_name: str):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=settings.rabbit_host))
        self.channel = self.connection.channel()
        self.queue_name = queue_name
        self.queue = self.channel.queue_declare(queue=queue_name, durable=True)
        self.exchange_name = exchange_name

    def send(self, message: bytes):
        self.channel.basic_publish(exchange=self.exchange_name, routing_key=self.queue_name, body=message)
