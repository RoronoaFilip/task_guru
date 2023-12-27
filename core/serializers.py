from rest_framework import serializers

from core.models.task import Task, Status


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'title', 'type', 'description', 'status', 'assignee', 'creator')

    def create(self, validated_data):
        open_status = Status.objects.get(status='OPEN')
        validated_data['status'] = open_status
        return super().create(validated_data)
