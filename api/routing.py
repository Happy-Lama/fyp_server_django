from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path("ws/transformer/data/", consumers.TransformerDataConsumer.as_asgi()),
    path("ws/transformer/specs/", consumers.TransformerSpecificationsConsumer.as_asgi()),
]