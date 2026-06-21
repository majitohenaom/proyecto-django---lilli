"""
ASGI config for mi_proyecto project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

if os.environ.get('DJANGO_SETTINGS_MODULE') == 'configuracion.settings':
    os.environ['DJANGO_SETTINGS_MODULE'] = 'mi_proyecto.settings'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mi_proyecto.settings')

application = get_asgi_application()
