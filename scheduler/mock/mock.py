"""
Имитация внешних сервисов.

"""
import uuid


class MockService:

    def __init__(self, batch_num: int = 2, batch_size: int = 3):
        self.batch_num = batch_num
        self.batch_size = batch_size

    def get_bookmarks(self) -> iter:
        for _ in range(self.batch_num):
            batch = [
                {'content': {'bookmarks': {}}, 'user_id': uuid.uuid4()}
                for _ in range(self.batch_size)
            ]
            yield batch

    def get_stats(self) -> iter:
        for _ in range(self.batch_num):
            batch = [
                {'content': {'stats': {}}, 'user_id': uuid.uuid4()}
                for _ in range(self.batch_size)
            ]
            yield batch

    def get_new_films(self) -> dict:
        return {}
