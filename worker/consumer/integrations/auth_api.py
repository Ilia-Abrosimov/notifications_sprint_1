"""Имитация ответа сервиса авторизации."""

import random

from faker import Faker
from pydantic import UUID4


class AuthAPI:
    """
    Класс интеграции с AUTH-сервисом.
    Предполагается, что существуют методы, позволяющие получить данные о часовом поясе пользователя и его email.
    """

    def __init__(self):
        self._faker = Faker()

    async def get_users_timezone(self, user_ids: list[UUID4]) -> dict[UUID4, int]:
        ret = {x: random.randint(-12, 12) for x in user_ids}
        return ret

    async def get_emails(self, recipients: list[UUID4]) -> dict[UUID4, str]:
        return {x: self._faker.ascii_email() for x in recipients}
