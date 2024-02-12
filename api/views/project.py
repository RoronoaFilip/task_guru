from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from core.decorators import content_type_json, log, except_and_then
from core.models.project import Project
from core.models.task import Task
from core.serializers import ProjectSerializer, TaskSerializer

EXCEPTION = Project.DoesNotExist


def and_then_callback():
    """Called after the exception is caught."""
    return Response(status=status.HTTP_404_NOT_FOUND)


@log
@except_and_then(EXCEPTION, and_then_callback)
@content_type_json
@api_view(['GET'])
def get_project_members(request, project_id, *args, **kwargs):
    """Returns all members for a given project by project_id."""
    project = Project.objects.get(id=project_id)
    members = project.members.all()
    return Response([{'id': member.id, 'username': member.username} for member in members],
                    status=status.HTTP_200_OK)


@log
@except_and_then(EXCEPTION, and_then_callback)
@content_type_json
@api_view(['GET'])
def get_project_tasks(request, project_id, *args, **kwargs):
    """Returns all tasks for a given project by project_id"""
    project = Project.objects.get(id=project_id)
    tasks = Task.objects.filter(project=project)
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


class ProjectView(APIView):
    @log
    @except_and_then(EXCEPTION, and_then_callback)
    def get(self, request, *args, **kwargs):
        project_id = kwargs.get('project_id')

        if project_id:
            project = Project.objects.get(id=project_id)
            serializer = ProjectSerializer(project)
        else:
            projects = Project.objects.all()
            serializer = ProjectSerializer(projects, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @log
    def post(self, request, *args, **kwargs):
        data = {}
        data['name'] = request.data.get('name', '')
        data['description'] = request.data.get('description', '')
        data['creator'] = User.objects.get(id=request.data.get('creatorId')).id if request.data.get(
            'creatorId') else None
        data['github_username'] = request.data.get('githubUsername', '')
        data['github_name'] = request.data.get('githubName', '')

        serializer = ProjectSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @log
    @except_and_then(EXCEPTION, and_then_callback)
    def patch(self, request, project_id):
        project = Project.objects.get(id=project_id)

        patch_data = {}
        patch_data['name'] = request.data.get('name', project.name)
        patch_data['description'] = request.data.get('description', project.description)
        patch_data['github_username'] = request.data.get('githubUsername', project.github_username)
        patch_data['github_name'] = request.data.get('githubName', project.github_name)

        serializer = ProjectSerializer(project, data=patch_data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @log
    @except_and_then(EXCEPTION, and_then_callback)
    def delete(self, request, project_id, *args, **kwargs):
        project = Project.objects.get(id=project_id)
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
