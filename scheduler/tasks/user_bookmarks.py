"""
Создание задания на рассылку напоминаний о закладках фильмов пользователя.

"""

from core.settings import mailing_settings

from messages.producers.scheduler.models import BookmarksMessage
from messages.schema.statuses import Statuses


class UserBookmarks:

    def __init__(self, service):
        self.service = service
        self.batch_size = mailing_settings.scheduler_batch_size

    def get_bookmarks(self) -> iter:
        """
        Предполагаем, что у аналитического сервиса есть метод get_bookmarks, возвращающий закладки
        пользователей партиями. При этом размер партии данных из сервиса может не совпадать
        с размером партии данных для обработки.
        """
        bookmarks = self.service.get_bookmarks()
        while True:
            try:
                data = next(bookmarks)
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
        bookmarks_data = self.get_bookmarks()
        while True:
            try:
                yield (
                    BookmarksMessage(recipients=[(item['user_id'])], status=Statuses.PREPARED, content=item['content'])
                    for item in next(bookmarks_data)
                )
            except StopIteration:
                break
