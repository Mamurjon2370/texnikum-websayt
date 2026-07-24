"""
WSGI config for texnikum project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'texnikum.settings')

application = get_wsgi_application()

# Vercel WSGI callable'ni "app" nomi bilan kutadi
app = application
