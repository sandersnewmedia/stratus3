from django import template
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.importlib import import_module
from django.utils.text import capfirst


register = template.Library()


def get_default_admin_site():
    path = getattr(settings, 'DEFAULT_ADMIN_SITE', 'django.contrib.admin.site')
    bits = path.split('.')
    attr = bits.pop()
    module = '.'.join(bits)

    try:
        mod = import_module(module)
    except ImportError:
        if settings.TEMPLATE_DEBUG:
            raise template.TemplateSyntaxtError('Module "%s" could not be '
                'found.' % module)
        return None

    try:
        return getattr(mod, attr)
    except AttributeError as e:
        if settings.TEMPLATE_DEBUG:
            raise template.TemplateSyntaxtError(e)
        return None


def get_navigation(context):
    apps = {}
    active = None

    if 'request' not in context:
        if settings.TEMPLATE_DEBUG:
            raise template.TemplateSyntaxError('Request must in the context '
                'to use navigation tags.')
        return apps, active

    request = context['request']
    user = request.user

    admin_site = get_default_admin_site()
    if admin_site is None:
        return apps, active

    for model, model_admin in admin_site._registry.items():
        label = model._meta.app_label
        perms = model_admin.get_model_perms(request)
        info = (label, model._meta.module_name)
        has_module_perms = user.has_module_perms(label)

        if has_module_perms and perms.get('change', False):
            url = reverse(
                viewname='admin:%s_%s_changelist' % info,
                current_app=admin_site.name,
            )

            model = {
                'name': capfirst(model._meta.verbose_name_plural),
                'url': url,
                'is_active': request.path.startswith(url),
            }

            if label in apps:
                apps[label]['models'].append(model)
            else:
                url = reverse(
                    viewname='admin:app_list',
                    kwargs={'app_label': label},
                    current_app=admin_site.name,
                )

                # This is a very naive way to do this, but it should work for now.
                is_active = request.path.startswith(url)
                if is_active:
                    active = label

                apps[label] = {
                    'name': label.title(),
                    'url': url,
                    'is_active': is_active,
                    'models': [model],
                }

    return apps, active


@register.inclusion_tag('stratus/navigation.html', takes_context=True)
def render_navigation(context):
    apps, active = get_navigation(context)
    return {
        'items': sorted(apps.values(), key=lambda o: o['name']),
    }


@register.inclusion_tag('stratus/navigation.html', takes_context=True)
def render_sub_navigation(context):
    apps, active = get_navigation(context)
    try:
        items = apps[active]['models']
    except KeyError:
        items = []
    return {
        'items': sorted(items, key=lambda o: o['name']),
        'classes': 'nav-tabs',
    }
