"""Admin panel."""
from datetime import datetime

from django.contrib import admin
from django.db.models import QuerySet

from .models import Message
from .producer import send_message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """Messages."""

    list_display = ['title', 'status']
    actions = ['set_status_sent']
    exclude = ('recipients',)

    @admin.action(description=('Отправить'))
    def set_status_sent(self, request, queryset: QuerySet):
        item: Message
        for item in queryset:
            if item.status != Message.StatusType.SENT:
                send_message(item.prepare_message())
        queryset.update(status=Message.StatusType.SENT, status_updated_at=datetime.now())
