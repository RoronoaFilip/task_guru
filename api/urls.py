from django.urls import path

from api.views.project import ProjectView, get_project_members
from api.views.task import TaskView

rest_api_urls = [
    path('tasks', TaskView.as_view()),
    path('tasks/<int:task_id>', TaskView.as_view()),
    path('projects', ProjectView.as_view()),
    path('projects/<int:project_id>', ProjectView.as_view()),
    path('projects/<int:project_id>/members', get_project_members),
]
