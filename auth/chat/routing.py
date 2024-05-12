from django.urls import path
from django.urls import re_path
from . import consumers
import chat.routing

websocket_urlpatterns = [
    # re_path(r'ws/socket-server/', consumers.ChatConsumer.as_asgi())
    # path('ws/join_game/', consumers.join_game.as_asgi()),
    path('ws/socket-server/', consumers.RacetCunsumer.as_asgi()),
]