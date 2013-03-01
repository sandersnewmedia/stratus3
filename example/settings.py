import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG
ROOT_URLCONF = 'urls'
WSGI_APPLICATION = 'wsgi.application'
SITE_ID = 1
SECRET_KEY = 'not-so-secret'
INTERNAL_IPS = ['127.0.0.1']

STATIC_URL = '/static/'

MEDIA_URL = '/uploads/'
MEDIA_ROOT = '/tmp/stratus/'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/tmp/stratus.db',
    }
}

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
)

INSTALLED_APPS = (
    'stratus',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'debug_toolbar',
    'people',
    'submissions',
)

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
}

TEMPLATE_DIRS = (os.path.join(os.path.dirname(__file__), 'templates'),)
