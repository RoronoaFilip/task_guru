from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


def send_task_update_event(project_id, task):
    channel_layer = get_channel_layer()
    task_dict = {
        'id': task.id,
        'title': task.title,
        'type': task.type.type,
        'status': task.status.status,
        'assignee': task.assignee.username if task.assignee else None,
    }
    async_to_sync(channel_layer.group_send)(
        f'project_{project_id}',
        {
            'type': 'update_task',
            'task': task_dict
        }
    )
