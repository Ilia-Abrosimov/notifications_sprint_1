import asyncio
from typing import Union

import backoff
from aio_pika import DeliveryMode, Message, connect_robust
from aiormq import ChannelInvalidStateError, ConnectionClosed
from pamqp.commands import Basic

from broker.core.settings import backoff_config, broker_settings
from broker.utils.logger import broker_logger


class Rabbit:

    def __init__(self, exchange_name: str, queue_name: str, prepare: bool = True):
        self.connection = None
        self.channel = None
        self.exchange = None
        self.queues = {}
        self.exchange_name = exchange_name
        self.queue_name = queue_name

        if prepare:
            # При работе через асихнронное Api подготовку брокера нужно вести через отдельный
            # вызов метода prepare. Поэтому экземпляр брокера создается с параметром False.
            # При работе через Админ-панель и планировщик настройки производятся сразу.
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self.prepare())

    @backoff.on_exception(**backoff_config, logger=broker_logger)
    async def connect(self):
        # Подключаемся к клиенту.
        self.connection = await connect_robust(broker_settings.broker_url)
        self.channel = await self.connection.channel()

    async def create_exchange(self, exchange_name: str):
        # Создаем точку обмена - лучше для каждого источника сообщений (Api, Admin, Scheduler)
        # сделать свою точку.
        self.exchange = await self.channel.declare_exchange(name=exchange_name)

    async def create_queue(self, queue_name: str):
        # Создаем очереди - основную и для отложенных сообщений (отстойник сообщений).
        queue = await self.channel.declare_queue(queue_name, durable=True)
        await queue.bind(exchange=self.exchange.name)

        delayed_queue = await self.channel.declare_queue(
            f'{queue_name}{broker_settings.suffix}',
            durable=True,
            arguments={
                'x-dead-letter-exchange': self.exchange.name,
                'x-dead-letter-routing-key': queue.name,
            })
        await delayed_queue.bind(exchange=self.exchange.name)
        self.queues.update({queue.name: queue, delayed_queue.name: delayed_queue})

    async def prepare(self):
        # Подготавливаем брокер - подкоючаемся к клиенту, создаем точку обмена и очереди.
        await self.connect()
        await self.create_exchange(self.exchange_name)
        await self.create_queue(self.queue_name)

    async def send(self, queue_name: str, message: bytes, expiration: int = 0) -> \
            Union[Basic.Ack, Basic.Nack, Basic.Reject, None]:
        # Отправляем сообщение в брокер. Если передан параметр expiration,
        # отправляем сообщение в отстойник.
        queue = f'{queue_name}{broker_settings.suffix}' if expiration else queue_name
        try:
            return await self.exchange.publish(
                Message(message, expiration=expiration, delivery_mode=DeliveryMode.PERSISTENT),
                routing_key=self.queues[queue].name,
            )
        except (ConnectionClosed, ChannelInvalidStateError):
            await self.prepare()

    async def receive(self, queue_name: str, callback):
        # Считываем сообщения из брокера.
        await self.queues[queue_name].consume(callback, no_ack=True)
        await asyncio.Future()
