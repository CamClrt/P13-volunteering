from .base import *  # noqa: F401, F403

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
]

INSTALLED_APPS += [  # noqa: F405
    # https://django-extensions.readthedocs.io/en/latest/
    "django_extensions",
    # https://django-debug-toolbar.readthedocs.io/en/latest/index.html
    "debug_toolbar",
]

MIDDLEWARE += [  # noqa: F405
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]
