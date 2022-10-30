"""
Управляющий файл для создания заданий на рассылки по расписанию.

"""

from mock.mock import MockService
from src.sender import Sender
from tasks.novelties import Novelties
from tasks.user_bookmarks import UserBookmarks
from tasks.user_stats import UserStats

from broker.base import BaseBroker
from messages.schema.exchanges import exchanges
from messages.schema.queues import scheduler_email_queues
from utils.injectors import broker_injector


class Manager:

    def __init__(self):
        self.sender = Sender()

    @broker_injector(exchange=exchanges.SCHEDULER, queue=scheduler_email_queues.NOVELTIES)
    def novelties(
            self,
            broker: BaseBroker,
            queue: str = scheduler_email_queues.NOVELTIES,
            service: MockService = MockService(),
    ):
        """ Получение списка новинок кинотеатра и создание одного сообщения для брокера,
        которое будет разослано всем пользователям. """
        novelties = Novelties(service)
        films = novelties.create_message()
        self.sender.send_one(broker, queue, films)

    @broker_injector(exchange=exchanges.SCHEDULER, queue=scheduler_email_queues.BOOKMARKS)
    def user_bookmarks(
            self,
            broker: BaseBroker,
            queue: str = scheduler_email_queues.BOOKMARKS,
            service: MockService = MockService(),
    ):
        """ Получение закладок пользователей и создание сообщений для каждого пользователя. """
        bookmarks = UserBookmarks(service)
        messages = bookmarks.create_messages()
        self.send_many(broker, queue, messages)

    @broker_injector(exchange=exchanges.SCHEDULER, queue=scheduler_email_queues.STATS)
    def user_stats(
            self,
            broker: BaseBroker,
            queue: str = scheduler_email_queues.STATS,
            service: MockService = MockService(),
    ):
        """ Получение периодической статистики пользователя и создание сообщений для каждого пользователя. """
        user_stats = UserStats(service)
        messages = user_stats.create_messages()
        self.send_many(broker, queue, messages)

    def send_many(self, broker: BaseBroker, queue: str, messages: iter) -> None:
        """ Отправка в брокер группы сообщений. """
        while True:
           try:
               batch = next(messages)
           except StopIteration:
               break
           else:
               self.sender.send_many(broker, queue, batch)
