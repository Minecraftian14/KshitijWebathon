import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "KshitijWebathon.settings")
django.setup()

from django.core.wsgi import get_wsgi_application
from . import mySecrets
from smartathon.views import sio

from socketio import WSGIApp
import eventlet
import eventlet.wsgi

print("Just a random number: ", 14)

if mySecrets.useSimpleTech:
    application = get_wsgi_application()

else:
    django_app = get_wsgi_application()
    application = WSGIApp(sio, django_app)

    eventlet.wsgi.server(eventlet.listen(('', 8000)), application)
