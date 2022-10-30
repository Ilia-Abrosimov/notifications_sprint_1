"""
Тестирование работы планировщика заданий на рассылку новых фильмов.

"""

import asyncio
import os
import sys
from threading import Thread

from aio_pika.abc import AbstractIncomingMessage
from orjson import orjson

from broker.rabbit import Rabbit
from messages.schema.exchanges import exchanges
from messages.schema.queues import scheduler_email_queues
from scheduler.manager import Manager

films = {'film_1': 'title', 'film_2': 'title'}


class MockService:

    def get_new_films(self) -> dict:
        return films


class BrokerConnector():

    def __init__(self):
        self.broker = None

    def producer(self):
        manager = Manager()
        manager.novelties(service=MockService())

    async def on_message(self, message: AbstractIncomingMessage):
        try:
            assert films == orjson.loads(message.body)['content']['films']
        except AssertionError:
            print('TEST FAILED')
        else:
            print('TEST PASSED')
        finally:
            try:
                sys.exit(0)
            except SystemExit:
                os._exit(0)

    def consumer(self):
        self.broker = Rabbit(exchange_name=exchanges.SCHEDULER, queue_name=scheduler_email_queues.NOVELTIES)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.broker.receive(queue_name=scheduler_email_queues.NOVELTIES, callback=self.on_message))


def test_user_stats_sent_to_broker():
    connector = BrokerConnector()

    t1 = Thread(target=connector.producer)
    t2 = Thread(target=connector.consumer)
    t1.start()
    t2.start()
    t1.join()
    t2.join()


test_user_stats_sent_to_broker()
