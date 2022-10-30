"""
Группы сообщений в рассылках.

"""

from enum import Enum


class ApiMessageTypes(Enum):
    SIGN_UP = 1
    REVIEW_LIKE = 2


class AdminMessageTypes(Enum):
    INFO = 1


class SchedulerMessageTypes(Enum):
    NOVELTIES = 1
    STATS = 2
    BOOKMARKS = 3
