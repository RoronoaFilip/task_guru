from django.contrib.auth.models import User

from core.models.project import Project
from core.models.task import Task, Status, Type


def create_user(username, password):
    user = User.objects.create_user(username=username, password=password)
    user.save()
    return user


def create_project(name, description, creator, github_username, github_name):
    project = Project.objects.create(name=name, description=description, creator=creator,
                                     github_username=github_username, github_name=github_name)
    project.save()
    project.members.add(creator)
    project.save()
    return project


def create_task(title, description, project, creator, status, task_type, assignee=None):
    assignee = assignee or creator
    task = Task.objects.create(title=title, description=description, project=project, creator=creator, status=status,
                               type=task_type, assignee=assignee)
    task.save()
    return task


def create_tasks(project, creator, status, task_type):
    task_1 = create_task('Test Task 1', 'Test Task Description 1', project, creator, status, task_type)
    task_2 = create_task('Test Task 2', 'Test Task Description 2', project, creator, status, task_type)
    task_3 = create_task('Test Task 3', 'Test Task Description 3', project, creator, status, task_type)
    return task_1, task_2, task_3


def create_type(type_name):
    task_type = Type.objects.create(type=type_name)
    task_type.save()
    return task_type


def create_status(status_name):
    status = Status.objects.create(status=status_name)
    status.save()
    return status
