"""
Инициаторы сообщений.

"""

from enum import Enum


class Senders(Enum):
    API = 1
    ADMIN = 2
    SCHEDULER = 3
