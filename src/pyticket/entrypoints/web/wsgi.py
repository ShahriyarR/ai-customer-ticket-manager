"""WSGI config for Django web entrypoint"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pyticket.configurator.settings")

application = get_wsgi_application()
