from django.db import models
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _


class BlockPage(models.Model):
    title = models.CharField(_('title'), max_length=100)
    description = models.TextField(_('description'), blank=True)
    keywords = models.TextField(_('keywords'), blank=True)
    url = models.CharField(_('URL'), max_length=100, db_index=True)
    template_name = models.CharField(_('template name'), max_length=70, default='blocks/blockpage.html')

    class Meta(object):
        db_table = 'stratus_blockpage'
        permissions = [
            ('change_url', 'Can change block url'),
            ('change_template_name', 'Can change block template name'),
        ]

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
    slug = models.SlugField(_('slug'))
    content_type = models.CharField(_('content type'), max_length=128, choices=CONTENT_TYPES)
    title = models.CharField(_('title'), max_length=256, unique=True)
    content = models.TextField(_('content'), blank=True)

    class Meta(object):
        db_table = 'stratus_block'
        unique_together = ['blockpage', 'slug']
        permissions = [
            ('change_title', 'Can change block title'),
            ('change_slug', 'Can change block slug'),
            ('change_content_type', 'Can change block content type'),
        ]

    def __unicode__(self):
        return '%s' % self.slug

    def render(self):
        if not self.content_type:
            return ''
        return render_to_string('blocks/block_%s.html' % self.content_type, {'block': self})
