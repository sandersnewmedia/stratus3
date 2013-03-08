from django.db import models
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _


class BlockPage(models.Model):
    title = models.CharField(_('title'), max_length=100)
    url = models.CharField(_('URL'), max_length=100, db_index=True)

    class Meta(object):
        db_table = 'stratus_blockpage'

    def __unicode__(self):
        return self.title


class Block(models.Model):
    CONTENT_TYPES = [
        ('single_line_text', _('Single Line Text')),
        ('multiple_line_text', _('Multiple Line Text')),
        ('html', _('Html')),
        ('image', _('Image')),
    ]

    blockpage = models.ForeignKey(BlockPage, verbose_name=_('page'), related_name='blocks')
    title = models.CharField(_('title'), max_length=256, unique=True)
    slug = models.SlugField(_('slug'))
    content_type = models.CharField(_('content type'), max_length=128, choices=CONTENT_TYPES)
    content = models.TextField(_('content'), blank=True)

    class Meta(object):
        db_table = 'stratus_block'
        unique_together = ['blockpage', 'slug']

    def __unicode__(self):
        return '%s' % self.slug

    def render(self):
        if not self.content_type:
            return ''
        return render_to_string('blocks/block_%s.html' % self.content_type, {'block': self})
