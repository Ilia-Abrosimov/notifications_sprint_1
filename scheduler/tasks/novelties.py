"""
Создание задания на рассылку о новинках в кинотеатре.

"""

from messages.producers.scheduler.models import NoveltiesMessage
from messages.schema.statuses import Statuses


class Novelties:

    def __init__(self, service):
        self.service = service

    def get_new_films(self) -> list:
        """
        Предполагаем, что у сервиса поиска фильмов есть метод get_new_films,
        возвращающий список новых фильмов.
        """
        return self.service.get_new_films()

    def create_message(self) -> NoveltiesMessage:
        """
        Преобразование полученных от сервиса поиска фильмов данных
        в готовое для отправки в брокер сообщение.
        """
        return NoveltiesMessage(status=Statuses.PREPARED, content={'films': self.get_new_films()})
