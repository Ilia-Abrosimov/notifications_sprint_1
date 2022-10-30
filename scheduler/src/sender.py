"""
Отправщик данных в брокер.

"""

import asyncio
import time

from orjson import orjson
from pamqp.commands import Basic

from broker.base import BaseBroker
from messages.producers.base import BaseMessage


class Sender:

    def send_one(self, broker: BaseBroker, queue: str, message: BaseMessage) -> None:
        loop = asyncio.get_event_loop()
        asyncio.set_event_loop(loop)
        sent = None
        min_sleep = 0.1
        while type(sent) is not Basic.Ack:
            sent = loop.run_until_complete(broker.send(queue, orjson.dumps(message.dict())))
            type(sent) is Basic.Ack or time.sleep(min_sleep := min_sleep * 2)

    def send_many(self, broker: BaseBroker, queue: str, messages: iter) -> None:
        loop = asyncio.get_event_loop()
        asyncio.set_event_loop(loop)
        messages_to_send = list(messages)
        min_sleep = 0.1
        while messages_to_send:
            # В брокер одновременно отправляется группа сообщений. В ответ возвращается список результатов
            # отправки. В случае, если в списке оказываются негативные результаты, осуществляется повтор
            # отправки только не доставленных в брокер сообщений.
            res = loop.run_until_complete(self.multiple_messages(broker, queue, messages_to_send))
            messages_to_send = list(
                item[0] for item
                in filter(lambda item: type(item[1]) is not Basic.Ack, zip(messages_to_send, res))
            )
            messages_to_send or time.sleep(min_sleep := min_sleep * 2)

    async def multiple_messages(self, broker: BaseBroker, queue: str, messages: iter) -> list:
        coroutines = [
            broker.send(
                queue_name=queue,
                message=orjson.dumps(message.dict())
            )
            for message in messages
        ]
        return await asyncio.gather(*coroutines, return_exceptions=True)
