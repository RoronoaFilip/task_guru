from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models.log import Log
from .models.project import Project
from .models.task import Task, Type, Status


class CustomUserAdmin(UserAdmin):
    list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('id', 'username', 'email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('id', 'username', 'email', 'first_name', 'last_name', 'is_staff')


class TaskAdmin(admin.ModelAdmin):
    model = Task
    list_display = (
        'id', 'title', 'type', 'description', 'status', 'assignee', 'creator', 'project')
    list_filter = ('id', 'type', 'status', 'assignee', 'creator', 'project')
    search_fields = ('id', 'title', 'type', 'description', 'assignee', 'creator', 'project')


class StatusAdmin(admin.ModelAdmin):
    model = Status
    list_display = ('id', 'status',)
    search_fields = ('id', 'status',)


class TypeAdmin(admin.ModelAdmin):
    model = Type
    list_display = ('id', 'type',)
    search_fields = ('id', 'type',)


class ProjectAdmin(admin.ModelAdmin):
    model = Project
    list_display = ('id', 'name', 'description', 'creator', 'github_username', 'github_name')
    list_filter = ('id', 'name', 'description', 'creator', 'members', 'github_username', 'github_name')
    search_fields = ('id', 'name', 'description', 'creator', 'members', 'github_username', 'github_name')


class LogAdmin(admin.ModelAdmin):
    model = Log
    list_display = ('id', 'user', 'request_method', 'request_uri',
                    'payload', 'response_status', 'response_payload', 'created')
    list_filter = ('id', 'user', 'request_method', 'request_uri',
                   'payload', 'response_status', 'response_payload', 'created')
    search_fields = ('id', 'user', 'request_method', 'request_uri',
                     'payload', 'response_status', 'response_payload', 'created')


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Status, StatusAdmin)
admin.site.register(Type, TypeAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Log, LogAdmin)
