from settings_base import *

DEBUG = True

INTERNAL_IPS += (
    '127.0.0.1',
)

# Depending on your environment, if you only need to override one database setting, this could be as simple as:
# DATABASES['default']['HOST'] = '123.123.123.123'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'currencies',
        'USER': 'web',
        'PASSWORD': 'web',
        'HOST': '127.0.0.1',
        'PORT': '',
    },
}

# Dump all emails to console so we don't risk sending emails
# when using production data
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Uncomment the following two lines to enable django-debug-toolbar:
INSTALLED_APPS += ('debug_toolbar', 'django_extensions',)
MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)


DEBUG_TOOLBAR_CONFIG = {
   'INTERCEPT_REDIRECTS' : False,
}


# Uncomment the following to enable devserver, see default settings below
# INSTALLED_APPS += ('devserver',)

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}
