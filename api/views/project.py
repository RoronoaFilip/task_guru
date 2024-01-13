from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from api.decorators import content_type_json, log
from core.models.project import Project
from core.models.task import Task
from core.serializers import ProjectSerializer, TaskSerializer


@log
@content_type_json
@api_view(['GET'])
def get_project_members(request, project_id, *args, **kwargs):
    """Returns all members for a given project by project_id."""
    try:
        project = Project.objects.get(id=project_id)
        members = project.members.all()
        return Response([{'id': member.id, 'username': member.username} for member in members],
                        status=status.HTTP_200_OK)
    except Project.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@log
@content_type_json
@api_view(['GET'])
def get_project_tasks(request, project_id, *args, **kwargs):
    """Returns all tasks for a given project by project_id"""
    try:
        project = Project.objects.get(id=project_id)
        tasks = Task.objects.filter(project=project)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Project.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


class ProjectView(APIView):
    @log
    def get(self, request, *args, **kwargs):
        task_id = kwargs.get('project_id')

        try:
            if task_id:
                task = Project.objects.get(id=task_id)
                serializer = ProjectSerializer(task)
            else:
                tasks = Project.objects.all()
                serializer = ProjectSerializer(tasks, many=True)
        except Project.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @log
    def post(self, request, *args, **kwargs):
        request.data['creator'] = User.objects.get(id=request.data.get('creator_id')).id if request.data.get(
            'creator_id') else None
        # request.data['members'] = []

        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @log
    def patch(self, request, project_id, *args, **kwargs):
        project = Project.objects.get(id=project_id)

        patch_data = {
            'name': request.data.get('name', project.name),
            'description': request.data.get('description', project.description),
            'members': request.data.get('members', project.members),
        }
        serializer = ProjectSerializer(project, data=patch_data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @log
    def delete(self, request, project_id, *args, **kwargs):
        try:
            project = Project.objects.get(id=project_id)
            project.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Project.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
