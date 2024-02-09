from django.urls import path

import api.views.project as project
import api.views.task as task
from api.views import github_proxy

rest_api_urls = [
    path('tasks', task.TaskView.as_view()),
    path('tasks/<int:task_id>', task.TaskView.as_view()),
    path('projects', project.ProjectView.as_view()),
    path('projects/<int:project_id>', project.ProjectView.as_view()),
    path('projects/<int:project_id>/members', project.get_project_members),
    path('projects/<int:project_id>/tasks', project.get_project_tasks),
    path('github/proxy', github_proxy.github_proxy, name='github_proxy'),
]
