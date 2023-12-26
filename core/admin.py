from django.contrib import admin

# Register your models here.
from .models import Task, Type, Status, Resolution


class TaskAdmin(admin.ModelAdmin):
    model = Task
    list_display = ('title', 'type', 'description', 'status', 'assignee', 'creator', 'modified', 'resolution', 'parent')
    list_filter = ('type', 'status', 'assignee', 'creator', 'modified', 'resolution', 'parent')
    search_fields = ('title', 'type', 'description', 'assignee', 'creator', 'modified', 'resolution', 'parent')


class StatusAdmin(admin.ModelAdmin):
    model = Status
    list_display = ('status',)
    search_fields = ('status',)


class TypeAdmin(admin.ModelAdmin):
    model = Type
    list_display = ('type',)
    search_fields = ('type',)


class ResolutionAdmin(admin.ModelAdmin):
    model = Resolution
    list_display = ('resolution',)
    search_fields = ('resolution',)


admin.site.register(Task, TaskAdmin)
admin.site.register(Status, StatusAdmin)
admin.site.register(Type, TypeAdmin)
admin.site.register(Resolution, ResolutionAdmin)
