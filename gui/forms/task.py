from django import forms

import sockets.utils.sockets_utils as sockets_utils
from core.models.task import Task


class TaskCreateForm(forms.ModelForm):
    def save(self, commit=True):
        task = super(TaskCreateForm, self).save(commit=False)
        if commit:
            task.save()
            sockets_utils.send_task_create_event(task.project.id, task)
        return task

    class Meta:
        model = Task
        fields = ['title', 'type', 'status', 'assignee', 'description']


class TaskUpdateForm(forms.ModelForm):
    def save(self, commit=True):
        task = super(TaskUpdateForm, self).save(commit=False)
        if commit:
            sockets_utils.send_task_update_event(task.project.id, task)
            task.save()
        return task

    class Meta:
        model = Task
        fields = ['title', 'type', 'status', 'assignee', 'description']
