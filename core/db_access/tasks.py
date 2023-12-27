from datetime import datetime

import core.db_access.users as user_service
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
        creator=user_service.find_user_by_id(creator_id),
    )

    return task


def find_task_by_id(task_id):
    """Find a Task by its ID."""
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return None

    return task


def find_all_tasks():
    """Find all Tasks."""
    tasks = Task.objects.all()

    return tasks


def update_task(task_id, update_dict):
    """Update a Task. """
    task = find_task_by_id(task_id)
    if not task:
        return None

    task.title = update_dict.get('title', task.title)
    task.type = find_type_by_name(update_dict.get('type', task.type.type))
    task.status = find_status_by_name(update_dict.get('status', task.status.status))
    task.description = update_dict.get('description', task.description)
    task.resolution = update_dict.get('resolution', task.resolution)
    task.assignee = update_dict.get('assignee', task.assignee)
    task.modified = datetime.now()
    task.save()

    return task


def patch_task(task_id, update_dict):
    """Patch a Task."""
    task = find_task_by_id(task_id)
    if not task:
        return None

    for field in ('type', 'status', 'resolution', 'assignee'):
        if field in update_dict:
            setattr(task, field, update_dict[field])

    task.modified = datetime.now()
    task.save()

    return task


def delete_task(task_id):
    """Delete a Task."""
    task = find_task_by_id(task_id)
    if not task:
        return None

    task.delete()

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
