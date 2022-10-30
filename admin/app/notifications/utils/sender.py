import asyncio
import time

import orjson
from pamqp.commands import Basic

from broker.base import BaseBroker
from messages.producers.base import BaseMessage


class Sender:
    @classmethod
    def send_one(cls, broker: BaseBroker, queue: str, message: BaseMessage) -> None:
        loop = asyncio.get_event_loop()
        asyncio.set_event_loop(loop)
        sent = None
        min_sleep = 0.1
        while type(sent) is not Basic.Ack:
            sent = loop.run_until_complete(broker.send(queue, orjson.dumps(message.dict())))
            type(sent) is Basic.Ack or time.sleep(min_sleep := min_sleep * 2)
