from rest_framework import serializers

from core.models.task import Task, Status


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'title', 'type', 'description', 'status', 'assignee', 'creator', 'project')
