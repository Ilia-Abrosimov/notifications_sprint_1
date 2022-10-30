"""
Базовая модель сообщений.

"""
import uuid
from datetime import datetime
from typing import List

from pydantic import BaseModel, Field

from messages.schema.channels import Channels
from messages.schema.senders import Senders
from messages.schema.statuses import Statuses


class BaseMessage(BaseModel):
    id: uuid.UUID = Field(title='id сообщения', default_factory=uuid.uuid4)
    created_at: datetime = Field(title='Время создания', default_factory=datetime.now)
    status_updated_at: datetime = Field(title='Время последнего обновления статуса', default_factory=datetime.now)
    channel: Channels = Field(title='Канал сообщения', default=Channels.EMAIL)
    status: Statuses = Field(title='Статус сообщения')
    recipients: List[uuid.UUID] = Field(title='Список получателей', default=[])
    content: dict = Field(title='Содержимое сообщения')
    check_timezone: bool = Field(title='Необходимость проверки таймзоны пользователя', default=True)
    check_relevance: bool = Field(title='Необходимость актуализации данных', default=True)
    sender: Senders = Field(title='Создатель сообщения')
