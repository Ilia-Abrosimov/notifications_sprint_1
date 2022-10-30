import uuid

from pydantic import BaseModel, Field


class BookmarksContent(BaseModel):
    bookmarks: dict = Field(title='Закладки фильмов')


class NoveltiesContent(BaseModel):
    films: dict = Field(title='Список новых фильмов')


class StatsContent(BaseModel):
    stats: dict = Field(title='Статистика пользователя')

