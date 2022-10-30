from messages.schema.exchanges import exchanges
from messages.schema.queues import admin_email_queues, api_email_queues, scheduler_email_queues

queues = [
    (exchanges.ADMIN, admin_email_queues.INFO),
    (exchanges.API, api_email_queues.SIGN_UP),
    (exchanges.API, api_email_queues.REVIEW_LIKE),
    (exchanges.SCHEDULER, scheduler_email_queues.BOOKMARKS),
    (exchanges.SCHEDULER, scheduler_email_queues.NOVELTIES),
    (exchanges.SCHEDULER, scheduler_email_queues.STATS),
]
