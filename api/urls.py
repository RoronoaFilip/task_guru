from django.urls import path

from api.views import tasks

rest_api_urls = [
    path('tasks', tasks.create_get_all),
    path('tasks/<int:task_id>', tasks.get_put_patch_delete),
]
