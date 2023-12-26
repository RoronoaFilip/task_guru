from datetime import datetime

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.decorators import content_type_json, accept_json
from core.db_access import tasks as tasks_service


@content_type_json
@accept_json
@api_view(['POST'])
def create_task(request):
    """Create a new Task object from a POST request."""
    task = tasks_service.create_task(
        title=request.data.get('title'),
        task_type=request.data.get('type'),
        description=request.data.get('description'),
        parent=request.data.get('parent'),
        assignee=request.data.get('assignee'),
        creator_id=request.data.get('creator_id'),
    )

    if not task:
        return Response({
            'error': 'Task could not be created'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({
        'id': task.id
    }, status=status.HTTP_201_CREATED)


@content_type_json
@api_view(['GET'])
def find_task(request, task_id):
    """Get a Task by its ID."""
    task = tasks_service.find_task_by_id(task_id)

    if not task:
        return Response({
            'error': 'Task not found'
        }, status=status.HTTP_404_NOT_FOUND)

    return Response({
        'id': task.id,
        'title': task.title,
        'type': task.type,
        'description': task.description,
        'status': task.status.status,
        'resolution': task.resolution.resolution,
        'parent': task.parent.id,
        'assignee': task.assignee,
        'creator': task.creator,
        'modified': task.modified
    }, status=status.HTTP_200_OK)
