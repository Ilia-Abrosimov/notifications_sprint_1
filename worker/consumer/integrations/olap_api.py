"""Имитация ответа сервиса аналитики."""

import random

from pydantic import UUID4


class OlapAPI:
    """
    Класс интеграции с OLAP-сервисом.
    Предполагается, что существуют методы, позволяющие получить необходимые данные по пользователям
    для подтверждения актуальности отправляемых данных и принятия решения об отправке сообщений.
    """

    async def check_relevance(self, user_ids: list[UUID4], *args) -> dict[UUID4, bool]:
        return {x: random.randint(0, 10) > 1 for x in user_ids}
