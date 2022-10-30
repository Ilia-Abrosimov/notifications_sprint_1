"""
Тестирование работы планировщика заданий на рассылку напоминаний о закладках.

"""

import asyncio
import os
import sys
import uuid
from threading import Thread

from aio_pika.abc import AbstractIncomingMessage
from orjson import orjson

from broker.rabbit import Rabbit
from messages.schema.exchanges import exchanges
from messages.schema.queues import scheduler_email_queues
from scheduler.manager import Manager

sent = []
received = []

BATCHES_NUM = 10
BATCH_SIZE = 20


class MockService:

    def get_bookmarks(self) -> iter:
        for _ in range(BATCHES_NUM):
            batch = [
                {'content': {'bookmarks': {'film_1': 'title', 'film_2': 'title'}}, 'user_id': uuid.uuid4()}
                for _ in range(BATCH_SIZE)
            ]
            sent.extend(batch)
            yield batch


class BrokerConnector():

    def __init__(self):
        self.counter = 0
        self.broker = None

    def producer(self):
        manager = Manager()
        manager.user_bookmarks(service=MockService())

    async def on_message(self, message: AbstractIncomingMessage):
        received.append(message.body)
        self.counter += 1
        if self.counter == BATCHES_NUM * BATCH_SIZE:
            try:
                assert [
                           (item['content'], str(item['user_id'])) for item in sent
                       ] == \
                       [
                           (orjson.loads(item)['content'], orjson.loads(item)['recipients'][0]) for item in received
                       ]
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
        self.broker = Rabbit(exchange_name=exchanges.SCHEDULER, queue_name=scheduler_email_queues.BOOKMARKS)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(
            self.broker.receive(
                queue_name=scheduler_email_queues.BOOKMARKS,
                callback=self.on_message
            )
        )


def test_user_bookmarks_sent_to_broker():
    connector = BrokerConnector()

    t1 = Thread(target=connector.producer)
    t2 = Thread(target=connector.consumer)
    t1.start()
    t2.start()
    t1.join()
    t2.join()


test_user_bookmarks_sent_to_broker()
