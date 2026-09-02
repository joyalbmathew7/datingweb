from django.urls import re_path

from chats.consumers import ChatConsumer
from notifications.consumers import NotificationConsumer


websocket_urlpatterns = [
    re_path(r"^ws/notifications/$", NotificationConsumer.as_asgi()),
    re_path(
        r"^ws/chats/(?P<uuid>[0-9a-f-]+)/$",
        ChatConsumer.as_asgi(),
    ),
]
