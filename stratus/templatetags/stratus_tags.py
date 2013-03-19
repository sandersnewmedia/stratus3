from django import template
from yawdadmin.templatetags.yawdadmin_tags import admin_top_menu

register = template.Library()

@register.inclusion_tag('admin/includes/appmenu.html', takes_context=True)
def admin_app_menu(context):
    return admin_top_menu(context)