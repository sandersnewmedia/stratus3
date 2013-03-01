from django.conf import settings


if 'django.contrib.auth' in settings.INSTALLED_APPS:
    from django.contrib.auth.admin import GroupAdmin, UserAdmin
    from django.contrib.auth.models import Group, User

    import stratus

    stratus.site.register(Group, GroupAdmin)
    stratus.site.register(User, UserAdmin)
