import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from posts.routing import websocket_urlpatterns  # ✅ Import WebSocket URLs

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "social.settings")

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": URLRouter(websocket_urlpatterns),  # ✅ WebSocket Routes
})
