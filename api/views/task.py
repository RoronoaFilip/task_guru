from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_api_key.permissions import HasAPIKey

from core.decorators import log, except_and_then
from core.models.project import Project
from core.models.task import Task, Type, Status
from core.serializers import TaskSerializer
from sockets.utils import sockets_utils

TASK_EXCEPTION = Task.DoesNotExist
STATUS_EXCEPTION = Status.DoesNotExist
TYPE_EXCEPTION = Type.DoesNotExist


def and_then_callback():
    """Called after the exception is caught."""
    return Response(status=status.HTTP_404_NOT_FOUND)


class TaskView(APIView):

    @log
    @except_and_then(TASK_EXCEPTION, and_then_callback)
    def get(self, request, *args, **kwargs):
        task_id = kwargs.get('task_id')

        if task_id:
            task = Task.objects.get(id=task_id)
            serializer = TaskSerializer(task)
        else:
            tasks = Task.objects.all()
            if len(tasks) == 0:
                return Response(status=204)
            serializer = TaskSerializer(tasks, many=True)

        return Response(serializer.data, status=200)

    @log
    def post(self, request, *args, **kwargs):
        post_data = extract_post_data(request.data)

        serializer = TaskSerializer(data=post_data)
        if serializer.is_valid():
            task = serializer.save()
            sockets_utils.send_task_create_event(post_data['project'], task)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    @log
    @except_and_then(TASK_EXCEPTION, and_then_callback)
    @except_and_then(TYPE_EXCEPTION, and_then_callback)
    @except_and_then(STATUS_EXCEPTION, and_then_callback)
    def patch(self, request, task_id, *args, **kwargs):
        task = Task.objects.get(id=task_id)

        assignee = request.data.get('assignee_id', None)
        if not assignee:
            assignee = task.assignee_id if task.assignee_id else None

        patch_data = extract_patch_data(request.data, task, assignee)

        serializer = TaskSerializer(task, data=patch_data, partial=True)
        if serializer.is_valid():
            task = serializer.save()
            sockets_utils.send_task_update_event(task.project.id, task)
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    @log
    @except_and_then(TASK_EXCEPTION, and_then_callback)
    def delete(self, request, task_id, *args, **kwargs):
        task = Task.objects.get(id=task_id)
        task.delete()
        sockets_utils.send_task_delete_event(task.project.id, task_id)
        return Response(status=200)


def extract_post_data(data_dict):
    """Extract the post_data from a Request data."""
    post_data = {
        'title': data_dict.get('title'), 'description': data_dict.get('description'),
        'type': Type.objects.get(type=data_dict.get('type')).id,
        'status': Status.objects.get(status='OPEN').id,
        'assignee': User.objects.get(id=data_dict.get('assigneeId')).id if data_dict.get('assigneeId') else None,
        'creator': User.objects.get(id=data_dict.get('creatorId')).id,
        'project': Project.objects.get(id=data_dict.get('projectId')).id
    }

    return post_data


def extract_patch_data(data_dict, task, assignee):
    """Extract the patch_data from a Request data."""
    patch_data = {
        'type': Type.objects.get(type=data_dict.get('type', task.type)).id,
        'status': Status.objects.get(status=data_dict.get('status', task.status)).id, 'assignee': assignee,
        'title': data_dict.get('title', task.title),
        'description': data_dict.get('description', task.description)
    }

    return patch_data
