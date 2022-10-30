"""
Создание задания на рассылку статистики пользователя.

"""

from core.settings import mailing_settings

from messages.producers.scheduler.models import StatsMessage
from messages.schema.statuses import Statuses


class UserStats:

    def __init__(self, service):
        self.service = service
        self.batch_size = mailing_settings.scheduler_batch_size

    def get_stats(self) -> iter:
        """
        Предполагаем, что у аналитического сервиса есть метод get_stats, возвращающий статистику
        пользователей партиями. При этом размер партии данных из сервиса может не совпадать
        с размером партии данных для обработки.
        """
        stats = self.service.get_stats()
        while True:
            try:
                data = next(stats)
            except StopIteration:
                break
            else:
                start, end, batch = 0, self.batch_size, True
                while batch:
                    yield (batch := data[start:end])
                    start, end = end, end + self.batch_size

    def create_messages(self) -> iter:
        """
        Преобразование полученных от аналитического сервиса данных
        в готовые для отправки в брокер сообщения.
        """
        stats_data = self.get_stats()
        while True:
            try:
                yield (
                    StatsMessage(recipients=[(item['user_id'])], status=Statuses.PREPARED, content=item['content'])
                    for item in next(stats_data)
                )
            except StopIteration:
                break
