from django import template


register = template.Library()


@register.assignment_tag
def can(user, permission, obj):
    perm = '%s.%s_%s' % (obj._meta.app_label, permission, obj._meta.module_name)
    return user.has_perm(perm)
