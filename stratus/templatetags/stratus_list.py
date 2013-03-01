from django import template
from django.conf import settings


register = template.Library()


@register.assignment_tag
def pluckobj(changelist, index):
    try:
        return changelist.result_list[index]
    except IndexError:
        if settings.TEMPLATE_DEBUG:
            raise
        return None
