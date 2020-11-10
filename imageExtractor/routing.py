from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import re_path

from imageExtractor import consumers

websocket_urlpatterns = [
    re_path(r'ws/extract/(?P<req_id>[^/]+)/$', consumers.RequestConsumer.as_asgi())
]
