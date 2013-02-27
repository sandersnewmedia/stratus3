from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class Submission(models.Model):
    STATUSES = [
        ('submitted', _('Submitted')),
        ('selected', _('Selected')),
        ('declined', _('Declined')),
        ('revoked', _('Revoked')),
    ]
    title = models.CharField(_('title'), max_length=255)
    status = models.CharField(_('status'), max_length=255, choices=STATUSES)
    created_date = models.DateTimeField(_('created date'), default=timezone.now)
