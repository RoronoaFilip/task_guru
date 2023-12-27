from django.contrib import admin
from django.urls import path, include

from api.urls import rest_api_urls

urlpatterns = [
    path('admin', admin.site.urls),
    path('api/', include(rest_api_urls), name='api'),
    path('', include('gui.urls')),
]
