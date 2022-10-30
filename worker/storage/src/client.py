"""
Подключение к БД для сохранения сообщений.

"""

import psycopg2
from psycopg2.extensions import connection as _connection
from psycopg2.extras import execute_values

from worker.storage.logger.logger import saver_logger


class StorageClient:

    def __init__(self, conn: _connection):
        self.conn = conn
        self.curs = conn.cursor()

    def save_data(self, data: list, table: str, fields: str) -> None:
        psycopg2.extras.register_uuid()
        query = f'INSERT INTO notifications.{table} ' \
                f'({fields}) ' \
                f'VALUES %s ON CONFLICT (id) DO NOTHING;'

        execute_values(self.curs, query, data)
        try:
            execute_values(self.curs, query, data)
        except Exception as error:
            saver_logger.error(f'Данные не были сохранены, {error}')
        else:
            self.conn.commit()
