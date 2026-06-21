"""
WSGI config for mi_proyecto project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

if os.environ.get('DJANGO_SETTINGS_MODULE') == 'configuracion.settings':
    os.environ['DJANGO_SETTINGS_MODULE'] = 'mi_proyecto.settings'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mi_proyecto.settings')

application = get_wsgi_application()
