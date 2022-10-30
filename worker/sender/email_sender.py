import json

from sendgrid import Mail, SendGridAPIClient

from messages.schema.statuses import Statuses
from worker.sender.base import BaseSander
from worker.sender.core.config import sender_settings
from worker.storage.src.saver import MessagesSaver


class SendgridSender(BaseSander):

    def __init__(self, client: SendGridAPIClient):
        super().__init__(client)

    async def send_one(self, message) -> int:
        email = Mail(
            from_email=sender_settings.mail_from,
            to_emails=message.recipient,  # TODO для дебага можно указать свою почту
            subject=json.loads(message.content)['subject'],
            plain_text_content=json.loads(message.content)['text'],
        )
        response = self.client.send(email)
        return response.status_code

    async def send(self, messages):

        for message in messages:
            response = await self.send_one(message)
            message.status = Statuses.SENT.name if response < 300 else Statuses.FAILED.name
        MessagesSaver.save(data=messages)


sendgrid_client = SendgridSender(client=SendGridAPIClient(sender_settings.sendgrid_api_key))
