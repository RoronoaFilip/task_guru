from django import forms
from django.contrib.auth.models import User

from core.models.project import Project


class ProjectCreateForm(forms.ModelForm):
    members = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.SelectMultiple,
        required=False
    )

    class Meta:
        model = Project
        fields = ['name', 'description', 'members', 'github_username', 'github_name']


class ProjectUpdateForm(forms.ModelForm):
    members = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.SelectMultiple,
        required=False
    )

    class Meta:
        model = Project
        fields = ['name', 'description', 'members', 'github_username', 'github_name']
