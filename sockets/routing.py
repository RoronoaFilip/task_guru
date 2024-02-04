from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/(?P<project_id>\w+)$', consumers.ProjectConsumer.as_asgi()),
]
