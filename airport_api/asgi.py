"""
ASGI config for airport_api project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

<<<<<<< HEAD
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'airport_api.settings')
=======
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "airport_api.settings")
>>>>>>> develop

application = get_asgi_application()
