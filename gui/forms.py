from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

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
        fields = ['name', 'description', 'members']


class TaskUpdateForm(forms.ModelForm):
    members = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.SelectMultiple,
        required=False
    )

    class Meta:
        model = Task
        fields = ['title', 'type', 'status', 'assignee', 'description']
