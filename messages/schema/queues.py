"""
Очереди сообщений.
"""


class BaseClass:

    def __init__(self):
        self.set_prefix()

    def set_prefix(self):
        for item in [
            attr for attr in dir(self)
            if not callable(getattr(self, attr))
               and not attr.startswith('__')
               and not attr == 'prefix'
        ]:
            setattr(self, item, f'{self.prefix}.{item.lower()}')


class ApiQueues(BaseClass):
    SIGN_UP = 'sign_up'
    REVIEW_LIKE = 'review_like'


class ApiEmailQueues(ApiQueues):
    prefix = 'email'


class AdminQueues(BaseClass):
    INFO = 'info'


class AdminEmailQueues(AdminQueues):
    prefix = 'email'


class SchedulerQueues(BaseClass):
    NOVELTIES = 'novelties'
    STATS = 'stats'
    BOOKMARKS = 'bookmarks'


class SchedulerEmailQueues(SchedulerQueues):
    prefix = 'email'


api_email_queues = ApiEmailQueues()
admin_email_queues = AdminEmailQueues()
scheduler_email_queues = SchedulerEmailQueues()
