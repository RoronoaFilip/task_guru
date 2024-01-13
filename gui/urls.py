from django.contrib.auth import views as auth_views
from django.urls import path

from gui import views

urlpatterns = [
    path('', views.home, name='home'),
    path('sockets_test', views.index, name='index'),
    path('projects', views.projects, name='projects'),
    path('projects/<int:project_id>', views.display_project, name='project'),
    path('projects/<int:project_id>/update', views.update_project, name='project'),
    path('tasks/<int:task_id>', views.get_task, name='task'),
    path('login', auth_views.LoginView.as_view()),
    path('register', views.register, name='register'),
    path('logout', views.logout, name='logout'),
]
