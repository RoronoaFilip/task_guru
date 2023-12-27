from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.decorators import content_type_json
from core.db_access import tasks as tasks_service
from core.models.task import Task


@content_type_json
@api_view(['POST', 'GET'])
def create_get_all(request):
    """Create a new Task object from a POST request."""
    if request.method == 'POST':
        return _create_task(request.data)
    elif request.method == 'GET':
        return _get_all_tasks()


@content_type_json
@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def get_put_patch_delete(request, task_id):
    """Get, update, patch, or delete a Task object. """
    if request.method == 'GET':
        return _get_task(task_id)
    elif request.method == 'PUT':
        return _update_task(task_id, request.data)
    elif request.method == 'PATCH':
        return _patch_task(task_id, request.data)
    elif request.method == 'DELETE':
        return _delete_task(task_id)


def _create_task(create_dict):
    task = tasks_service.create_task(
        title=create_dict.get('title'),
        task_type=create_dict.get('type'),
        description=create_dict.get('description'),
        parent=create_dict.get('parent'),
        assignee=create_dict.get('assignee'),
        creator_id=create_dict.get('creator_id'),
    )

    if not task:
        return Response({
            'error': 'Task could not be created'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({
        'id': task.id
    }, status=status.HTTP_201_CREATED)


def _get_task(task_id):
    task = tasks_service.find_task_by_id(task_id)

    if not task:
        return Response({
            'error': 'Task not found'
        }, status=status.HTTP_404_NOT_FOUND)

    return _task_response(task)


def _get_all_tasks():
    tasks = tasks_service.find_all_tasks()

    return _task_response(list(tasks))


def _update_task(task_id, update_dict):
    task = tasks_service.update_task(task_id, update_dict)

    if not task:
        return Response({
            'error': 'Task could not be updated'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return _task_response(task)


def _patch_task(task_id, update_dict):
    task = tasks_service.patch_task(task_id, update_dict)

    if not task:
        return Response({
            'error': 'Task could not be updated'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return _task_response(task)


def _delete_task(task_id):
    task = tasks_service.delete_task(task_id)

    if not task:
        return Response({
            'error': 'Task could not be deleted'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(status=status.HTTP_200_OK)


def _task_response(task: Task | list[Task]):
    if isinstance(task, list):
        response_data = [construct_task_dict(t) for t in task]
        return Response(response_data,
                        status=status.HTTP_200_OK if len(response_data) > 0 else status.HTTP_204_NO_CONTENT)
    else:
        return Response(construct_task_dict(task), status=status.HTTP_200_OK)


def construct_task_dict(task):
    """Construct a dictionary from a Task object."""
    return {
        'id': task.id,
        'title': task.title,
        'type': task.type.type,
        'status': task.status.status,
        'description': task.description,
        'parent_id': task.parent_id,
        'assignee_id': task.assignee_id,
        'creator_id': task.creator_id,
        'modified': task.modified
    }
