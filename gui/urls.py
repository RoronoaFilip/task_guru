from django.contrib.auth import views as auth_views
from django.urls import path

from gui.views import project, task, auth

urlpatterns = [
    path('', auth.home, name='home'),
    path('projects', project.get_projects, name='projects'),
    path('projects/<int:project_id>', project.get_project, name='project'),
    path('projects/<int:project_id>/update', project.update_project, name='project'),
    path('projects/create', project.create_project, name='project'),
    path('tasks/<int:task_id>', task.get_task_page, name='task'),
    path('tasks/<int:task_id>/card', task.get_task, name='task'),
    path('tasks/<int:task_id>/update', task.update_task, name='task'),
    path('tasks/<int:project_id>/create', task.create_task, name='task'),
    path('login', auth_views.LoginView.as_view(), name='login'),
    path('register', auth.register, name='register'),
    path('logout', auth.logout, name='logout'),
]
