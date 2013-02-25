from django import template
from django.contrib.admin.templatetags import admin_list


register = template.Library()


@register.inclusion_tag('stratus/date_hierarchy.html')
def date_hierarchy(cl):
    return admin_list.date_hierarchy(cl)


@register.inclusion_tag('stratus/search_form.html')
def search_form(cl):
    return admin_list.search_form(cl)


@register.simple_tag
def admin_list_filter(cl, spec):
    return admin_list.admin_list_filter(cl, spec)


@register.inclusion_tag('stratus/actions.html', takes_context=True)
def admin_actions(context):
    return admin_list.admin_actions(context)


@register.inclusion_tag('stratus/change_list_results.html')
def result_list(cl):
    return admin_list.result_list(cl)


@register.simple_tag
def paginator_number(cl, i):
    return admin_list.paginator_number(cl, i)


@register.inclusion_tag('stratus/pagination.html')
def pagination(cl):
    return admin_list.pagination(cl)
