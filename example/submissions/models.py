from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class Submission(models.Model):
    STATUSES = [
        ('submitted', _('Submitted')),
    ]
    title = models.CharField(_('title'), max_length=255)
    status = models.CharField(_('status'), max_length=255, choices=STATUSES)
    created_date = models.DateTimeField(_('created date'), default=timezone.now)


class SubmissionEstimate(models.Model):
    user = models.ForeignKey(User, verbose_name=_('user'))
    submission = models.ForeignKey(Submission, verbose_name=_('submission'), related_name='estimates')
    value = models.IntegerField(_('value'), default=0)
    created_date = models.DateTimeField(_('created date'), default=timezone.now)

    class Meta(object):
        ordering = ['value']
        unique_together = ['user', 'submission']
