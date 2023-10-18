import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.environment.{}".format(os.environ['ENVIRONMENT']))

application = get_wsgi_application()

