from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.shortcuts import render


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
