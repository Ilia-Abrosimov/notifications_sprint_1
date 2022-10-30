"""
Статусы сообщений.

PREPARED - готово к отправке (такой статус у сообщения при его создании).
POSTPONED - отложено в случае, если настройки таймзоны пользователя не позволяют отправить ему сообщение сейчас.
SENT - отправлено.
RECEIVED - доставлено.
CANCELED - отмена отправки, если информация в сообщении устарела.
FAILED - ошибка отправки.
"""

from enum import Enum


class Statuses(Enum):
    PREPARED = 1
    POSTPONED = 2
    SENT = 3
    RECEIVED = 4
    CANCELED = 5
    FAILED = 6
