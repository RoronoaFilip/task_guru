from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from django.shortcuts import render

from core.decorators import log
from core.models.project import Project
from core.models.task import Task
from gui.forms import project as project_forms


@log
@login_required(login_url='/login')
def get_projects(request):
    """Projects page view render."""
    user = request.user
    projects = Project.objects.filter(members=user)
    return render(request, 'projects/projects.html', {
        'user': request.user,
        'projects': projects,
    })


@log
@login_required(login_url='/login')
def create_project(request):
    """Create project view."""
    if request.method == 'POST':
        new_project = Project()
        new_project.creator = request.user
        form = project_forms.ProjectCreateForm(request.POST, instance=new_project)
        if form.is_valid():
            new_project = form.save(request.user)
            new_project.members.add(request.user)
            new_project.save()
            return redirect('projects')
    else:
        form = project_forms.ProjectCreateForm()
    return render(request, 'form.html', {'form': form, 'action': 'Create', 'item': 'Project'})


@log
@login_required(login_url='/login')
def update_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.method == 'POST':
        form = project_forms.ProjectUpdateForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('projects')
    else:
        form = project_forms.ProjectUpdateForm(instance=project)

    return render(request, 'form.html', {'form': form, 'action': 'Update', 'item': 'Project'})


@log
@login_required(login_url='/login')
def get_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    tasks = Task.objects.filter(project=project)

    open_tasks = tasks.filter(status__status='OPEN')
    in_progress_tasks = tasks.filter(status__status='IN PROGRESS')
    done_tasks = tasks.filter(status__status='DONE')

    return render(request, 'projects/project.html', {
        'project': project,
        'tasks': tasks,
        'open_tasks': open_tasks,
        'in_progress_tasks': in_progress_tasks,
        'done_tasks': done_tasks,
    })
