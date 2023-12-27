from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework.views import APIView

from core.models.task import Task, Type, Status
from core.serializers import TaskSerializer


class TaskView(APIView):
    def get(self, request, *args, **kwargs):
        task_id = kwargs.get('task_id')

        try:
            if task_id:
                task = Task.objects.get(id=task_id)
                serializer = TaskSerializer(task)
            else:
                tasks = Task.objects.all()
                if len(tasks) == 0:
                    return JsonResponse(status=204)
                serializer = TaskSerializer(tasks, many=True)
        except Task.DoesNotExist:
            return JsonResponse(status=404)

        return JsonResponse(serializer.data, status=200)

    def post(self, request, *args, **kwargs):
        serializer = TaskSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors)

    def patch(self, request, task_id, *args, **kwargs):
        task = Task.objects.get(id=task_id)
        request.data['type'] = Type.objects.get(type=request.data.get('type', task.type)).id
        request.data['status'] = Status.objects.get(status=request.data.get('status', task.status)).id
        request.data['assignee'] = User.objects.get(id=request.data.get('assignee_id', task.assignee_id)).id
        serializer = TaskSerializer(task, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=200)
        return JsonResponse(serializer.errors, status=400)

    def delete(self, request, task_id, *args, **kwargs):
        task = Task.objects.get(id=task_id)
        task.delete()
        return JsonResponse(status=200)
