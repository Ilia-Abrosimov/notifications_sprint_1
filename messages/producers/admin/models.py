"""
Модели сообщений, отправленных через Admin Panel.

"""
from pydantic import Field

from messages.schema.categories import AdminMessageTypes
from messages.schema.senders import Senders

from ..base import BaseMessage


class AdminBaseMessage(BaseMessage):
    sender: Senders = Field(title='Создатель сообщения', default=Senders.ADMIN)


class InfoMessage(AdminBaseMessage):
    """ Информационное сообщение. """
    group: AdminMessageTypes = Field(title='Группа сообщения', default=AdminMessageTypes.INFO)
    template: str = Field(title='Шаблон сообщения', default='base.html')
