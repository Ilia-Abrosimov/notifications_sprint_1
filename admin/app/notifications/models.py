"""Models."""

import uuid
from datetime import datetime
from typing import Optional

from django.db import models
from django.utils.translation import gettext_lazy as _
from notifications.producer import send_message
from notifications.utils.utils import UUID4Validator
from pydantic import parse_obj_as

from messages.producers.admin.models import InfoMessage
from messages.schema.categories import AdminMessageTypes
from messages.schema.channels import Channels
from messages.schema.statuses import Statuses


class TimeStampedMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Message(UUIDMixin, TimeStampedMixin):
    """Сообщение"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._original_status = self.status
        self._original_recipients_file = self.recipients_file

    class StatusType(models.IntegerChoices):
        DRAFT = 1, _('Draft')
        SAVED = 2, _('Saved')
        SENT = 3, _('Sent')

    class ChannelType(models.IntegerChoices):
        EMAIL = Channels.EMAIL.value, _('email')
        WEB_NOTIFICATION = Channels.WEB_NOTIFICATION.value, _('web')
        APP_NOTIFICATION = Channels.APP_NOTIFICATION.value, _('app')
        SMS = Channels.SMS.value, _('sms')

    class MessageType(models.IntegerChoices):
        INFO = AdminMessageTypes.INFO.value, _('info')

    title = models.CharField(_('title'), max_length=255)
    description = models.TextField(_('description'), blank=True, null=True)
    recipients = models.JSONField(_('recipients'), blank=True, null=True)
    recipients_file = models.FileField(_('recipients'), null=True, upload_to='uploads/')
    content = models.TextField(_('content'))
    status = models.IntegerField(_('status'), choices=StatusType.choices, default=StatusType.DRAFT)
    status_updated_at = models.DateTimeField(auto_now_add=True)
    channel = models.IntegerField(_('channel'), choices=ChannelType.choices, default=ChannelType.EMAIL)
    check_timezone = models.BooleanField(_('timezone checking'), default=1)
    check_relevance = models.BooleanField(_('relevance checking'), default=1)
    group = models.IntegerField(_('message group'), choices=MessageType.choices, default=AdminMessageTypes.INFO.value)
    template = models.FileField(_('template'), blank=True, null=True, default='base.html', upload_to='uploads/')

    def __str__(self):
        return self.title

    def prepare_message(self) -> Optional[InfoMessage]:
        values = {k: self.__dict__[k] for k in InfoMessage.__dict__.get('__fields__') if k in self.__dict__}
        now = datetime.now()
        values['created_at'] = now
        values['status_updated_at'] = now
        values['status'] = Statuses.PREPARED.value
        values['content'] = {'message': self.content}
        values['recipients'] = UUID4Validator(uuids=self.recipients).uuids
        values['template'] = f'{self.template}'
        return parse_obj_as(InfoMessage, values)

    def save(self, *args, **kwargs):
        if self.recipients_file and self.recipients_file != self._original_recipients_file:
            ids = self.recipients_file.file.readlines()
            ids = UUID4Validator(uuids=[x.decode('utf-8').strip() for x in ids])
            self.recipients = [str(x) for x in ids.uuids]

            # emails = self.recipients_file.file.readlines()
            # emails = EmailValidator(emails=emails)
            # self.recipients = emails.emails

        if self.status != self._original_status:
            self.status_updated_at = datetime.now()
            if self.status == self.StatusType.SENT:
                send_message(self.prepare_message())

        super().save(*args, **kwargs)

    class Meta:
        db_table = 'notifications"."messages'
        verbose_name = _('message')
        verbose_name_plural = _('messages')
