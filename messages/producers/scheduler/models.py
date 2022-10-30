"""
Модели сообщений, отправленных через планировщик.

"""
from pydantic import Field

from messages.schema.categories import SchedulerMessageTypes
from messages.schema.senders import Senders

from ..base import BaseMessage
from .content import BookmarksContent, NoveltiesContent, StatsContent


class SchedulerBaseMessage(BaseMessage):
    sender: Senders = Field(title='Создатель сообщения', default=Senders.SCHEDULER)


class BookmarksMessage(SchedulerBaseMessage):
    """ Рассылка напоминаний о закладках фильмов. """
    group: SchedulerMessageTypes = Field(title='Группа сообщения', default=SchedulerMessageTypes.BOOKMARKS)
    template: str = Field(title='Шаблон сообщения', default='base.html')
    content: BookmarksContent = Field(title='Содержимое сообщения')


class NoveltiesMessage(SchedulerBaseMessage):
    """ Рассылка новых фильмов. """
    group: SchedulerMessageTypes = Field(title='Группа сообщения', default=SchedulerMessageTypes.NOVELTIES)
    template: str = Field(title='Шаблон сообщения', default='base.html')
    content: NoveltiesContent = Field(title='Содержимое сообщения')


class StatsMessage(SchedulerBaseMessage):
    """ Рассылка статистики пользователя. """
    group: SchedulerMessageTypes = Field(title='Группа сообщения', default=SchedulerMessageTypes.STATS)
    template: str = Field(title='Шаблон сообщения', default='base.html')
    content: StatsContent = Field(title='Содержимое сообщения')
