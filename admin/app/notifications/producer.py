from notifications.utils.sender import Sender

from broker.base import BaseBroker
from messages.producers.admin.models import InfoMessage
from messages.schema.exchanges import exchanges
from messages.schema.queues import admin_email_queues
from utils.injectors import broker_injector


@broker_injector(exchange=exchanges.ADMIN, queue=admin_email_queues.INFO)
def send_message(item: InfoMessage, broker: BaseBroker, queue=admin_email_queues.INFO):
    Sender.send_one(broker, queue, item)
