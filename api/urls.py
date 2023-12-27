from django.urls import path

from api.views.task import TaskView

rest_api_urls = [
    path('tasks', TaskView.as_view()),
    path('tasks/<int:task_id>', TaskView.as_view()),
]
