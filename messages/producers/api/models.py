"""
Модели сообщений, отправленных через Api.

"""
from pydantic import EmailStr, Field

from messages.schema.categories import ApiMessageTypes
from messages.schema.senders import Senders

from ..base import BaseMessage


class ApiBaseMessage(BaseMessage):
    sender: Senders = Field(title='Создатель сообщения', default=Senders.API)


class SignUpMessage(ApiBaseMessage):
    """ Сообщение после регистрации пользователя. """
    group: ApiMessageTypes = Field(title='Группа сообщения', default=ApiMessageTypes.SIGN_UP)
    template: str = Field(title='Шаблон сообщения', default='base.html')


class ReviewLikeMessage(ApiBaseMessage):
    """ Сообщение об оценке обзору пользователя. """
    group: ApiMessageTypes = Field(title='Группа сообщения', default=ApiMessageTypes.REVIEW_LIKE)
    template: str = Field(title='Шаблон сообщения', default='base.html')
