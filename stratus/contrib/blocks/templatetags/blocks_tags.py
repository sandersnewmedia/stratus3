from django import template
from django.conf import settings
from django.utils.html import mark_safe


register = template.Library()


@register.simple_tag
def renderblock(slug, blockpage):
    if not hasattr(blockpage, '_cached_block_dict'):
        blockpage._cached_block_dict = {b.slug: b for b in blockpage.blocks.all()}

    try:
        block = blockpage._cached_block_dict[slug]
    except KeyError as e:
        if settings.TEMPLATE_DEBUG:
            raise e
        return ''

    return mark_safe(block.render())
