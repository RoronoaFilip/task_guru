import markdown2 as markdown
from django.contrib.auth import logout as django_logout, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from django.shortcuts import render

from core.decorators import log
from core.models.project import Project
from core.models.task import Task
from gui import forms


@log
def register(request):
    """Register view."""
    if request.method == "POST":
        form = forms.RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = forms.RegisterUserForm()
    context = {
        'form': form,
    }
    return render(request, 'registration/register.html', context)


@log
@login_required(login_url='/login')
def logout(request):
    """Logout view."""
    django_logout(request)
    return redirect('/login')


@log
@login_required(login_url='/login')
def home(request):
    """Home page view render."""
    return render(request, 'main/home.html', {
        'user': request.user,
    })


@log
@login_required(login_url='/login')
def projects(request):
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
        form = forms.ProjectCreateForm(request.POST, instance=new_project)
        if form.is_valid():
            new_project = form.save(request.user)
            new_project.members.add(request.user)
            new_project.save()
            return redirect('projects')
    else:
        form = forms.ProjectCreateForm()
    return render(request, 'form.html', {'form': form, 'action': 'Create', 'item': 'Project'})


@log
@login_required(login_url='/login')
def update_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.method == 'POST':
        form = forms.ProjectUpdateForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('projects')
    else:
        form = forms.ProjectUpdateForm(instance=project)

    return render(request, 'form.html', {'form': form, 'action': 'Update', 'item': 'Project'})


@log
@login_required(login_url='/login')
def display_project(request, project_id):
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
        form = forms.TaskCreateForm(request.POST, instance=new_task)
        if form.is_valid():
            task = form.save()
            return redirect(f'/projects/{task.project.id}')
    else:
        form = forms.TaskCreateForm()
    return render(request, 'form.html', {'form': form, 'action': 'Create', 'item': 'Task'})


@log
@login_required(login_url='/login')
def update_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == 'POST':
        form = forms.TaskUpdateForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect(f'/projects/{task.project.id}')
    else:
        form = forms.TaskUpdateForm(instance=task)

    return render(request, 'form.html', {'form': form, 'action': 'Update', 'item': 'Task'})
