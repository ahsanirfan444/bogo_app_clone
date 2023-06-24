from django.urls import re_path

from web_socket.consumers import MapSocketConsumer, ChatSocketConsumer


websocket_urlpatterns = [
    re_path('ws/mysocket/', MapSocketConsumer.as_asgi()),
    re_path('ws/chat_socket/', ChatSocketConsumer.as_asgi()),
]


