"""Development settings."""

import socket

DEBUG = True

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'debug_toolbar',
    'notifications.apps.NotificationsConfig',
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
INTERNAL_IPS = [ip[: ip.rfind('.')] + '.1' for ip in ips] + ['127.0.0.1', '10.0.2.2']

DEBUG_TOOLBAR_CONFIG = {'SHOW_TOOLBAR_CALLBACK': lambda request: False if request.is_ajax() else True}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'filters': {'require_debug_true': {'()': 'django.utils.log.RequireDebugTrue', }},
    'formatters': {'default': {'format': '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]', }, },
    'handlers': {
        'debug-console': {'class': 'logging.StreamHandler', 'formatter': 'default',
                          'filters': ['require_debug_true'], },
    },
    'loggers': {'django.db.backends': {'level': 'DEBUG', 'handlers': ['debug-console'], 'propagate': False, }},
}
