"""
Модели в таблице истории сообщений.

"""

import uuid
from datetime import datetime

from pydantic import BaseSettings, EmailStr, Field


class EmailMessage(BaseSettings):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    created_at: datetime = Field(title='Время создания сообщения')
    updated_at: datetime = Field(title='Время последнего обновления')
    status: str = Field(title='Статус сообщения')
    sender: str = Field(title='Источник создания сообщения')
    recipient: EmailStr = Field(title='Получатель')
    content: bytes = Field(title='Содержимое сообщения')
