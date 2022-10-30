"""
Декоратор, определяющий брокер для Api, Admin Panel, Scheduler и Worker.

"""
import functools

from broker.rabbit import Rabbit


def broker_injector(exchange: str = None, queue: str = None):
    # Депоратор для админ-панели и планировщика.
    def inner(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            exchange_name = exchange or kwargs.get('exchange')
            queue_name = queue or kwargs.get('queue')
            broker = Rabbit(exchange_name=exchange_name, queue_name=queue_name)
            return func(*args, broker=broker, **kwargs)

        return wrapper

    return inner


def api_broker_injector(exchange: str = None, queue: str = None):
    # Депоратор для Flask Api с асинхронностью.
    def inner(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            exchange_name = exchange or kwargs.get('exchange')
            queue_name = queue or kwargs.get('queue')
            broker = Rabbit(exchange_name=exchange_name, queue_name=queue_name, prepare=False)
            await broker.prepare()
            return await func(*args, broker=broker, **kwargs)

        return wrapper

    return inner
