from django.contrib import admin

# Register your models here.
from .models.task import Task, Type, Status, Resolution
from .models.user import TaskGuruUser


class TaskGuruUserAdmin(admin.ModelAdmin):
    model = TaskGuruUser
    list_display = ('id', 'username', 'password', 'email', 'first_name', 'last_name')
    search_fields = ('id', 'username', 'password', 'email', 'first_name', 'last_name')


class TaskAdmin(admin.ModelAdmin):
    model = Task
    list_display = (
        'id', 'title', 'type', 'description', 'status', 'assignee', 'creator', 'modified', 'resolution', 'parent')
    list_filter = ('id', 'type', 'status', 'assignee', 'creator', 'modified', 'resolution', 'parent')
    search_fields = ('id', 'title', 'type', 'description', 'assignee', 'creator', 'modified', 'resolution', 'parent')


class StatusAdmin(admin.ModelAdmin):
    model = Status
    list_display = ('id', 'status',)
    search_fields = ('id', 'status',)


class TypeAdmin(admin.ModelAdmin):
    model = Type
    list_display = ('id', 'type',)
    search_fields = ('id', 'type',)


class ResolutionAdmin(admin.ModelAdmin):
    model = Resolution
    list_display = ('id', 'resolution',)
    search_fields = ('id', 'resolution',)


admin.site.register(TaskGuruUser, TaskGuruUserAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Status, StatusAdmin)
admin.site.register(Type, TypeAdmin)
admin.site.register(Resolution, ResolutionAdmin)
