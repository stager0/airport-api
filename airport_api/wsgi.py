"""
WSGI config for airport_api project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

<<<<<<< HEAD
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'airport_api.settings')
=======
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "airport_api.settings")
>>>>>>> develop

application = get_wsgi_application()
