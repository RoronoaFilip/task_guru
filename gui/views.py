from django.contrib.auth import logout as django_logout, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from django.shortcuts import render

from core.models.project import Project
from gui.forms import RegisterUserForm, ProjectUpdateForm


def register(request):
    """Register view."""
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = RegisterUserForm()
    context = {
        'form': form,
    }
    return render(request, 'registration/register.html', context)


@login_required(login_url='/login')
def logout(request):
    """Logout view."""
    django_logout(request)
    return redirect('/login')


@login_required(login_url='/login')
def index(request):
    """Sockets page."""
    return render(request, 'sockets_index.html', {
        'group_name': 'test',
    })


@login_required(login_url='/login')
def home(request):
    """Home page view render."""
    return render(request, 'main/home.html', {
        'user': request.user,
    })


@login_required(login_url='/login')
def projects(request):
    """Projects page view render."""
    user = request.user
    projects = Project.objects.filter(members=user)
    return render(request, 'main/projects.html', {
        'user': request.user,
        'projects': projects,
    })


@login_required(login_url='/login')
def update_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.method == 'POST':
        form = ProjectUpdateForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('projects')
    else:
        form = ProjectUpdateForm(instance=project)

    return render(request, 'project/project_update.html', {'form': form, 'project': project})
