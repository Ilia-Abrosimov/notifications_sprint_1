"""
Каналы отправки сообщений.
"""

from enum import Enum


class Channels(Enum):
    EMAIL = 1
    WEB_NOTIFICATION = 2
    APP_NOTIFICATION = 3
    SMS = 4
