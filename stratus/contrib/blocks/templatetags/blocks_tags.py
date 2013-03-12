from django import template
from django.conf import settings
from django.utils.html import mark_safe

from stratus.contrib.blocks.models import Block


register = template.Library()


@register.simple_tag
def renderblock(slug, blockpage=None):
    if blockpage is None:
        try:
            return mark_safe(Block.objects.filter(slug__startswith=slug)[0].render())
        except KeyError as e:
            if settings.TEMPLATE_DEBUG:
                raise e
        return ''

    if not hasattr(blockpage, '_cached_block_dict'):
        blockpage._cached_block_dict = {b.slug: b for b in blockpage.blocks.all()}

    try:
        block = blockpage._cached_block_dict[blockpage.slug + '-' + slug]

    except KeyError as e:
        if settings.TEMPLATE_DEBUG:
            raise e
        return ''

    return mark_safe(block.render())
