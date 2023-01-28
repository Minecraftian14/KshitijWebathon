"""
WSGI config for KshitijWebathon project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

from . import mySecrets
from smartathon.views import sio

from socketio import WSGIApp

import eventlet
import eventlet.wsgi

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "KshitijWebathon.settings")

if mySecrets.useSimpleTech:
    application = get_wsgi_application()

else:
    django_app = get_wsgi_application()
    application = WSGIApp(sio, django_app)

    eventlet.wsgi.server(eventlet.listen(('', 8000)), application)
