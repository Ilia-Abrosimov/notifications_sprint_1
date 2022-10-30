import asyncio
import datetime
import uuid

import orjson
import pandas as pd
import pytz
from aio_pika.abc import AbstractIncomingMessage
from loguru import logger
from pamqp.commands import Basic
from pydantic import parse_obj_as

from broker.rabbit import Rabbit
from messages.producers.base import BaseMessage
from messages.schema.statuses import Statuses
from utils.injectors import broker_injector
from worker.consumer.integrations.auth_api import AuthAPI
from worker.consumer.integrations.olap_api import OlapAPI
from worker.sender.email_sender import BaseSander
from worker.storage.models.models import EmailMessage
from worker.storage.src.saver import MessagesSaver


class Consumer:
    def __init__(self, auth_api: AuthAPI, olap_api: OlapAPI, sender: BaseSander):
        self._auth_api = auth_api
        self._olap_api = olap_api
        self._sender = sender
        self._broker = None
        self._queue = None

    @broker_injector()
    def run_receiver(self, exchange: str, queue: str, broker: Rabbit) -> None:
        self._broker = broker
        self._queue = queue
        loop = asyncio.get_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(broker.receive(queue_name=queue, callback=self._receiver_callback))

    async def _receiver_callback(self, message: AbstractIncomingMessage) -> None:
        body = parse_obj_as(BaseMessage, orjson.loads(message.body))
        logger.info(f'{body.id = }')
        body = await self._filter_by_timezones(body)
        body = await self._filter_by_relevance(body)
        await self._send_to_worker(body)

    async def _filter_by_relevance(self, body: BaseMessage) -> BaseMessage:
        if not body.check_relevance:
            return body
        recipients = await self._olap_api.check_relevance(body.recipients)
        users_df = pd.DataFrame(recipients.items(), columns=['id', 'ok'])
        ok_users = users_df[users_df.ok == 1].id.to_list()
        delete_users = users_df[users_df.ok == 0].id.to_list()

        if delete_users:
            body.recipients = delete_users
            await self.cancel_messages(body)

        body.recipients = ok_users
        return body

    async def _filter_by_timezones(self, body: BaseMessage) -> BaseMessage:
        if not body.check_timezone:
            return body
        grouped_users = {}
        utc_now_dt = datetime.datetime.now(tz=pytz.UTC)
        users_with_timezones = await self._auth_api.get_users_timezone(body.recipients)
        users_df = pd.DataFrame(users_with_timezones.items(), columns=['id', 'tz'])
        users_df['delay_diff'] = users_df['tz'].apply(self._get_delay, args=(utc_now_dt,))
        grouped = users_df.groupby(by='delay_diff')
        groups = grouped.groups
        for delay in groups:
            grouped_users[delay] = users_df.iloc[groups[delay]].id.to_list()

        delaies = [x for x in grouped_users.keys() if x]
        logger.info(f'Prepare {len(delaies)} messages to broker')

        for delay in delaies:
            delayed_body = body.copy(deep=True)
            delayed_body.recipients = grouped_users[delay]
            await self.return_to_broker(delayed_body, int(f'{delay}'))
        logger.info(f'Sent to broker: {len(delaies)}')

        if 0 in grouped_users:
            body.recipients = grouped_users[0]
        return body

    def _get_delay(self, tz: int, utc_now_dt: datetime.datetime) -> int:
        start_hour = 9
        end_our = 21

        users_time = utc_now_dt + datetime.timedelta(hours=tz)
        if start_hour <= users_time.hour < end_our:
            return 0
        if start_hour < users_time.hour:
            return datetime.timedelta(hours=start_hour - users_time.hour - 1, minutes=60 - users_time.minute).seconds
        else:
            return datetime.timedelta(
                hours=start_hour + 24 - users_time.hour - 1, minutes=60 - users_time.minute
            ).seconds

    async def _message_prepare(self, body: BaseMessage, status: Statuses) -> list[EmailMessage]:
        recipients_emails = await self._auth_api.get_emails(body.recipients)
        values = {k: body.__dict__[k] for k in body.__dict__ if k in EmailMessage.__fields__}
        values['updated_at'] = datetime.datetime.now()
        values['status'] = status.name
        values['sender'] = body.sender.name
        values['content'] = orjson.dumps(body.content)
        messages = []
        for recipient in recipients_emails.values():
            values['id'] = uuid.uuid4()
            values['recipient'] = recipient
            messages.append(parse_obj_as(EmailMessage, values))
        return messages

    async def cancel_messages(self, body: BaseMessage) -> None:
        messages = await self._message_prepare(body, Statuses.CANCELED)
        MessagesSaver.save(data=messages)
        logger.info(f'Canceled messages for {len(messages)} users: {[message.recipient for message in messages]}')

    async def return_to_broker(self, body: BaseMessage, delay: int) -> None:
        message = body.dict()
        message['status'] = Statuses.POSTPONED
        min_sleep = 0.1
        sent = None
        while type(sent) is not Basic.Ack:
            sent = await self._broker.send(queue_name=self._queue, message=orjson.dumps(message), expiration=delay)
            type(sent) is Basic.Ack or await asyncio.sleep(min_sleep := min_sleep * 2)

    async def _send_to_worker(self, body: BaseMessage) -> None:
        messages = await self._message_prepare(body, Statuses.PREPARED)
        logger.info(f'Sent messages for {len(messages)} users: {[message.recipient for message in messages]}')
        await self._sender.send(messages)
