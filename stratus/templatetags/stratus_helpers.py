from django import template
from django.conf import settings
from django.db.models import get_models


register = template.Library()

@register.inclusion_tag('stratus/help_text.html')
def render_app_help_text(app_list):
    lookup = {}
    for model in get_models():
        lookup[model._meta.verbose_name_plural.lower()] = (
            model._meta.app_label,
            '%s.%s' % (model._meta.app_label, model._meta.module_name),
        )

    help_text = getattr(settings, 'STRATUS_HELP_TEXT', {})
    blocks = set()

    for app in app_list:
        for model in app['models']:
            for key in lookup.get(model['name'].lower()):
                if key in help_text:
                    blocks.add(help_text[key].strip())

    return {'blocks': blocks}
