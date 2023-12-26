from django.contrib.auth import views as auth_views
from django.urls import path

from gui import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', auth_views.LoginView.as_view()),
    path('logout', auth_views.LogoutView.as_view()),
]
