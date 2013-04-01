from django.db import models
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _

from stratus.validators import validate_key


class BlockGroup(models.Model):
    title = models.CharField(_('title'), max_length=100)
    key = models.CharField(_('key'), max_length=50, unique=True, validators=[validate_key])

    class Meta(object):
        db_table = 'stratus_blockgroup'
        permissions = [
            ('change_key', 'Can change block group key'),
        ]

    def __unicode__(self):
        return self.title


class Block(models.Model):
    CONTENT_TYPES = [
        ('single_line_text', _('Single Line Text')),
        ('multiple_line_text', _('Multiple Line Text')),
        ('list_text', _('List Text')),
        ('html', _('Html')),
    ]

    group = models.ForeignKey(BlockGroup, verbose_name=_('group'), related_name='blocks')
    key = models.CharField(_('key'), max_length=50, validators=[validate_key])
    content_type = models.CharField(_('content type'), max_length=128, choices=CONTENT_TYPES)
    content = models.TextField(_('content'), blank=True)

    class Meta(object):
        db_table = 'stratus_block'
        unique_together = ['group', 'key']
        permissions = [
            ('change_key', 'Can change block key'),
            ('change_content_type', 'Can change block content type'),
        ]

    def __unicode__(self):
        return self.key.replace('_', ' ').title()

    def render(self, request=None):
        if not self.content_type:
            content = ''
        else:
            content = render_to_string('blocks/block_%s.html' % self.content_type, {'block': self})

        if request and '_preview' in request.GET and request.user.is_staff:
            return render_to_string('blocks/block_wrapper.html', {
                'block': self,
                'content': content,
            })
        else:
            return content
