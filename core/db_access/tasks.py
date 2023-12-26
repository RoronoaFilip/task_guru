from django.contrib.auth.models import User

from core.models.task import Task, Status, Type


def create_task(title, task_type, description, parent, assignee, creator_id):
    """Create a new Task object."""
    task = Task.objects.create(
        title=title,
        type=Type.objects.get(type=task_type),
        description=description,
        status=Status.objects.get(status='OPEN'),
        resolution=None,
        parent=parent,
        assignee=assignee,
        creator=User.objects.get(id=creator_id),
    )

    return task


def find_task_by_id(task_id):
    """Find a Task by its ID."""
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return None

    return task


def find_type_by_name(type_name):
    """Find a Task by its Name."""
    try:
        task_type = Type.objects.get(type=type_name)
    except Type.DoesNotExist:
        return None

    return task_type


def find_status_by_name(status_name):
    """Find a Task by its Name."""
    try:
        status = Status.objects.get(status=status_name)
    except Status.DoesNotExist:
        return None

    return status

