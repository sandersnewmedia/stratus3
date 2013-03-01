from django.contrib.admin.templatetags.admin_list import *  # NOQA
from django.contrib.admin.templatetags.admin_list import register, result_list as admin_result_list
from django.template.loader import render_to_string


@register.simple_tag(takes_context=True)
def result_list(context, cl):
    app_label = cl.model._meta.app_label
    module_name = cl.model._meta.module_name

    template_names = [
        'stratus/%s/%s/change_list_results.html' % (app_label, module_name),
        'stratus/%s/change_list_results.html' % app_label,
        'stratus/change_list_results.html',
        getattr(cl.model_admin, 'change_list_results_template', 'admin/change_list_results.html'),
    ]

    context.update(admin_result_list(cl))
    return render_to_string(template_names, context)
