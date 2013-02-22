from django import template
from django.contrib.admin.templatetags import admin_list, admin_modify


register = template.Library()


@register.inclusion_tag('stratus/submit_line.html', takes_context=True)
def submit_row(context):
    return admin_modify.submit_row(context)


@register.inclusion_tag('stratus/change_list_results.html')
def result_list(cl):
    return admin_list.result_list(cl)


@register.inclusion_tag('stratus/pagination.html')
def pagination(cl):
    return admin_list.pagination(cl)
