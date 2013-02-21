from django.conf import settings


defaults = {
    'STRATUS_BASE_URL': '/admin/dashboard/',
    'STRATUS_LOGIN_URL': '/admin/login/',
}


def get(name):
    return getattr(settings, name, defaults.get(name))
