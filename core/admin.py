from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models.task import Task, Type, Status


class CustomUserAdmin(UserAdmin):
    list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'is_staff')


class TaskAdmin(admin.ModelAdmin):
    model = Task
    list_display = (
        'id', 'title', 'type', 'description', 'status', 'assignee', 'creator')
    list_filter = ('id', 'type', 'status', 'assignee', 'creator')
    search_fields = ('id', 'title', 'type', 'description', 'assignee', 'creator')


class StatusAdmin(admin.ModelAdmin):
    model = Status
    list_display = ('id', 'status',)
    search_fields = ('id', 'status',)


class TypeAdmin(admin.ModelAdmin):
    model = Type
    list_display = ('id', 'type',)
    search_fields = ('id', 'type',)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Status, StatusAdmin)
admin.site.register(Type, TypeAdmin)
