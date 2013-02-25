from django.template import Library
from django.contrib.admin.templatetags import admin_static


register = Library()


@register.simple_tag
def static(path):
    return admin_static.static(path)
