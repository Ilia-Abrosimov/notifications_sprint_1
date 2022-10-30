"""
Преобразование параметров запроса.

"""

from functools import wraps

from flask import request


def unpack_models(f):
    """Декоратор который входные модели укладывает в kwargs функции."""

    @wraps(f)
    def decorated_function(*args, **kwargs):

        if (body := request.context.body) is not None:
            kwargs.update({'body': body})

        if (query := request.context.query) is not None:
            kwargs.update({'query': query})

        if (headers := request.context.headers) is not None:
            kwargs.update({'headers': headers})

        return f(*args, **kwargs)

    return decorated_function
