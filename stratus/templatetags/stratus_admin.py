from django import template
from django.contrib.admin.templatetags.admin_list import (
    pagination as admin_pagination,
    results,
    result_headers,
    result_hidden_fields,
)


register = template.Library()


@register.inclusion_tag('stratus/submit_line.html', takes_context=True)
def submit_row(context):
    """
    Displays the row of buttons for delete and save.
    """
    opts = context['opts']
    change = context['change']
    is_popup = context['is_popup']
    save_as = context['save_as']
    return {
        'onclick_attrib': opts.get_ordered_objects() and change and 'onclick="submitOrderForm();"' or '',
        'show_delete_link': not is_popup and context['has_delete_permission'] and (change or context['show_delete']),
        'show_save_as_new': not is_popup and change and save_as,
        'show_save_and_add_another': context['has_add_permission'] and not is_popup and (not save_as or context['add']),
        'show_save_and_continue': not is_popup and context['has_change_permission'],
        'is_popup': is_popup,
        'show_save': True,
    }


@register.inclusion_tag('stratus/change_list_results.html')
def result_list(cl):
    """
    Displays the headers and data list together

    """
    headers = list(result_headers(cl))
    num_sorted_fields = 0

    for h in headers:
        if h['sortable'] and h['sorted']:
            num_sorted_fields += 1

    return {
        'cl': cl,
        'result_hidden_fields': list(result_hidden_fields(cl)),
        'result_headers': headers,
        'num_sorted_fields': num_sorted_fields,
        'results': list(results(cl)),
    }


@register.inclusion_tag('stratus/pagination.html')
def pagination(cl):
    return admin_pagination(cl)
