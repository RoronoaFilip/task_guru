from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.decorators import log
from core.models.project import Project
from core.models.task import Task, Type, Status
from core.serializers import TaskSerializer


class TaskView(APIView):

    @log
    def get(self, request, *args, **kwargs):
        task_id = kwargs.get('task_id')

        try:
            if task_id:
                task = Task.objects.get(id=task_id)
                serializer = TaskSerializer(task)
            else:
                tasks = Task.objects.all()
                if len(tasks) == 0:
                    return Response(status=204)
                serializer = TaskSerializer(tasks, many=True)
        except Task.DoesNotExist:
            return Response(status=404)

        return JsonResponse(serializer.data, status=200)

    @log
    def post(self, request, *args, **kwargs):
        post_data = {
            'title': request.data.get('title'),
            'description': request.data.get('description'),
            'type': Type.objects.get(type=request.data.get('type')).id,
            'status': Status.objects.get(status='OPEN').id,
            'assignee': User.objects.get(id=request.data.get('assignee_id')).id if request.data.get(
                'assignee_id') else None,
            'creator': User.objects.get(id=request.data.get('creator_id')).id,
            'project': Project.objects.get(id=request.data.get('project_id')).id,
        }
        serializer = TaskSerializer(data=post_data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

    @log
    def patch(self, request, task_id, *args, **kwargs):
        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            return Response(status=404)

        assignee = request.data.get('assignee_id', None)
        if not assignee:
            assignee = task.assignee_id if task.assignee_id else None

        patch_data = {
            'type': Type.objects.get(type=request.data.get('type', task.type)).id,
            'status': Status.objects.get(status=request.data.get('status', task.status)).id,
            'assignee': assignee,
            'title': request.data.get('title', task.title),
            'description': request.data.get('description', task.description),
        }
        serializer = TaskSerializer(task, data=patch_data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=200)
        return JsonResponse(serializer.errors, status=400)

    @log
    def delete(self, request, task_id, *args, **kwargs):
        try:
            task = Task.objects.get(id=task_id)
            task.delete()
            return Response(status=200)
        except Task.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
