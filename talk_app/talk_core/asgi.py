"""
ASGI config for talk_core project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "talk_core.settings")

import django

django.setup()

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from chat.service.middleware import AuthSocketMiddleware
from channels.auth import  AuthMiddleware

import chat.routing

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AuthSocketMiddleware(URLRouter(chat.routing.websocket_urlpatterns)),
    }
)
