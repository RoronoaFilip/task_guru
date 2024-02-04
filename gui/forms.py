from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

import sockets.utils.sockets_utils as sockets_utils
from core.models.project import Project
from core.models.task import Task


class RegisterUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email",
                  "password1", "password2")


class ProjectUpdateForm(forms.ModelForm):
    members = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.SelectMultiple,
        required=False
    )

    class Meta:
        model = Project
        fields = ['name', 'description', 'members', 'github_username', 'github_name']


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
