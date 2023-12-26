from django.urls import path

from api.views import tasks

rest_api_urls = [
    path('tasks', tasks.create_task, name='create_task'),
    path('tasks/<int:task_id>', tasks.find_task, name='get_task'),
]
