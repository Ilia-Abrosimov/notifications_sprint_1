"""
Сохранение сообщений в БД истории.

"""

from contextlib import contextmanager

import psycopg2
from psycopg2.extras import DictCursor

from worker.storage.core.settings import storage_settings
from worker.storage.models.models import EmailMessage
from worker.storage.src.client import StorageClient


@contextmanager
def pg_conn_context():
    conn = psycopg2.connect(**storage_settings, cursor_factory=DictCursor)
    yield conn
    conn.close()


class MessagesSaver:

    @staticmethod
    def save(data: list, table: str = 'email'):
        fields = ', '.join(tuple(EmailMessage.__fields__.keys()))
        with pg_conn_context() as pg_conn:
            saver = StorageClient(pg_conn)
            saver.save_data(
                data=[tuple(message.dict().values()) for message in data],
                table=table,
                fields=fields,
            )
