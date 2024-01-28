from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


def send_task_create_event(project_id, task):
    """Send a task create event to the project group."""
    _send_event(project_id, 'task_create', 'task', _to_dict(task))


def send_task_update_event(project_id, task):
    """Send a task update event to the project group."""
    _send_event(project_id, 'task_update', 'task', _to_dict(task))


def send_task_delete_event(project_id, task_id):
    """Send a task delete event to the project group."""
    _send_event(project_id, 'task_delete', 'task', {'id': task_id})


def _to_dict(task):
    """Convert a task to a dict."""
    return {
        'id': task.id,
        'title': task.title,
        'description': task.description,
        'type': task.type.type,
        'status': task.status.status,
        'assignee': task.assignee.username if task.assignee else None,
        'project_id': task.project.id
    }


def _send_event(project_id, event_type, field, data):
    """Send an event to the project group."""
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f'project_{project_id}',
        {
            'type': event_type,
            field: data
        }
    )
