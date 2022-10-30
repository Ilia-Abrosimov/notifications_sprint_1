"""
Преобразование pydantic.BaseModel в json.

"""

from functools import wraps

from flask import jsonify


def json_response(f):
    """Декоратор который после выполнения функции из Response-модели делает json и возвращает ее."""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        result_dict = f(*args, **kwargs)
        return jsonify(**result_dict.dict(by_alias=True))

    return decorated_function
