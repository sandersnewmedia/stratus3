from django import template


register = template.Library()


@register.inclusion_tag('stratus/navigation.html')
def render_navigation(navigation):
    return {
        'items': sorted(navigation['apps'].values(), key=lambda o: o['name']),
    }


@register.inclusion_tag('stratus/navigation.html')
def render_sub_navigation(navigation):
    if navigation['active']:
        try:
            items = navigation['apps'][navigation['active']]['models']
        except IndexError:
            items = []
    else:
        items = []

    return {
        'items': sorted(items, key=lambda o: o['name']),
        'classes': 'nav-tabs',
    }
