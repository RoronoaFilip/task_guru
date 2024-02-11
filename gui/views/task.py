import markdown2 as markdown
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from django.shortcuts import render

from core.decorators import log
from core.models.project import Project
from core.models.task import Task
from gui.forms import task as task_forms


@log
@login_required(login_url='/login')
def get_task(request, task_id):
    """Task box view render."""
    task = get_object_or_404(Task, id=task_id)
    return render(request, 'tasks/task.html', {
        'id': task.id,
        'title': task.title,
        'type': task.type.type,
        'status': task.status.status,
        'assignee': task.assignee,
    })


@log
@login_required(login_url='/login')
def get_task_page(request, task_id):
    """Task page view render."""
    task = get_object_or_404(Task, id=task_id)
    description = markdown.markdown(task.description)
    return render(request, 'tasks/task_page.html', {
        'id': task.id,
        'title': task.title,
        'type': task.type.type,
        'status': task.status.status,
        'description': description,
        'assignee': task.assignee,
        'project_id': task.project.id,
    })


@log
@login_required(login_url='/login')
def create_task(request, project_id):
    if request.method == 'POST':
        new_task = Task()
        new_task.project = Project.objects.get(id=project_id)
        new_task.creator = request.user
        form = task_forms.TaskCreateForm(request.POST, instance=new_task)
        if form.is_valid():
            task = form.save()
            return redirect(f'/projects/{task.project.id}')
    else:
        form = task_forms.TaskCreateForm()
    return render(request, 'form.html', {'form': form, 'action': 'Create', 'item': 'Task'})


@log
@login_required(login_url='/login')
def update_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == 'POST':
        form = task_forms.TaskUpdateForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect(f'/projects/{task.project.id}')
    else:
        form = task_forms.TaskUpdateForm(instance=task)

    return render(request, 'form.html', {'form': form, 'action': 'Update', 'item': 'Task'})
