from django import template
from django.conf import settings
from django.utils.html import mark_safe

from stratus.blocks.models import Block


register = template.Library()


@register.simple_tag
def renderblock(slug, blockpage=None):
    if blockpage:
        try:
            block = blockpage.blocksdict()[slug]
        except KeyError:
            block = None
    else:
        try:
            block = Block.objects.get(slug=slug)
        except Block.DoesNotExist:
            block = None

    if block:
        return mark_safe(block.render())
    elif settings.TEMPLATE_DEBUG:
        return "[block '%s' does not exist]" % slug
    else:
        return ''
