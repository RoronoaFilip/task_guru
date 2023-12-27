from django.urls import path

import api.views.project as project
from api.views.task import TaskView

rest_api_urls = [
    path('tasks', TaskView.as_view()),
    path('tasks/<int:task_id>', TaskView.as_view()),
    path('projects', project.ProjectView.as_view()),
    path('projects/<int:project_id>', project.ProjectView.as_view()),
    path('projects/<int:project_id>/members', project.get_project_members),
    path('projects/<int:project_id>/tasks', project.get_project_tasks),
]
