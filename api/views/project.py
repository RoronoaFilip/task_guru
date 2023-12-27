from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models.project import Project
from core.serializers import ProjectSerializer


@api_view(['GET'])
def get_project_members(request, project_id, *args, **kwargs):
    project = Project.objects.get(id=project_id)
    members = project.members.all()
    return Response([{'id': member.id, 'username': member.username} for member in members],
                    status=200 if len(members) > 0 else 204)


class ProjectView(APIView):
    def get(self, request, *args, **kwargs):
        task_id = kwargs.get('project_id')

        try:
            if task_id:
                task = Project.objects.get(id=task_id)
                serializer = ProjectSerializer(task)
            else:
                tasks = Project.objects.all()
                if len(tasks) == 0:
                    return Response(status=204)
                serializer = ProjectSerializer(tasks, many=True)
        except Project.DoesNotExist:
            return Response(status=404)

        return Response(serializer.data, status=200)

    def post(self, request, *args, **kwargs):
        request.data['creator'] = User.objects.get(id=request.data.get('creator_id')).id if request.data.get(
            'creator_id') else None
        # request.data['members'] = []

        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

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
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    def delete(self, request, project_id, *args, **kwargs):
        project = Project.objects.get(id=project_id)
        project.delete()
        return Response(status=200)
