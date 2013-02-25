from django import template
from django.contrib.admin.templatetags import admin_modify


register = template.Library()


@register.inclusion_tag('stratus/prepopulated_fields_js.html', takes_context=True)
def prepopulated_fields_js(context):
    return admin_modify.prepopulated_fields_js(context)


@register.inclusion_tag('stratus/submit_line.html', takes_context=True)
def submit_row(context):
    return admin_modify.submit_row(context)


@register.filter
def cell_count(inline_admin_form):
    return admin_modify.cell_count(inline_admin_form)
