from concurrent.futures.thread import ThreadPoolExecutor

from sendgrid import SendGridAPIClient

from messages.schema.exchanges import exchanges
from messages.schema.queues import admin_email_queues
from worker.consumer.consumer import Consumer
from worker.consumer.integrations.auth_api import AuthAPI
from worker.consumer.integrations.olap_api import OlapAPI
from worker.consumer.queues_data import queues
from worker.sender.core.config import sender_settings
from worker.sender.email_sender import BaseSander, SendgridSender


def receive(exchange: exchanges, queue: admin_email_queues, auth: AuthAPI, olap: OlapAPI, sender: BaseSander):
    consumer = Consumer(auth_api=auth, olap_api=olap, sender=sender)
    consumer.run_receiver(exchange=exchange, queue=queue)


if __name__ == '__main__':
    auth_ = AuthAPI()
    olap_ = OlapAPI()
    sender_ = SendgridSender(client=SendGridAPIClient(sender_settings.sendgrid_api_key))

    with ThreadPoolExecutor(max_workers=len(queues)) as executor:
        futures = [executor.submit(receive, exchange, queue, auth_, olap_, sender_) for exchange, queue in queues]
