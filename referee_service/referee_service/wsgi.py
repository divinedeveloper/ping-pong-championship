"""
WSGI config for referee_service project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os
import json

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "referee_service.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
