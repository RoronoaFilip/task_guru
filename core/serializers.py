from rest_framework import serializers

from core.models.project import Project
from core.models.task import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'title', 'type', 'description', 'status', 'assignee', 'creator', 'project')


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('id', 'name', 'description', 'creator', 'github_username', 'github_name')

    def create(self, validated_data):
        project = Project.objects.create(**validated_data)
        project.members.add(validated_data.get('creator'))
        project.save()
        return project
