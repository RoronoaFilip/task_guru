from django.contrib.auth import logout as django_logout, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.shortcuts import render

from core.decorators import log
from gui.forms import auth as auth_forms


@log
def register(request):
    """Register view."""
    if request.method == "POST":
        form = auth_forms.RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = auth_forms.RegisterUserForm()
    return render(request, 'form.html', {'form': form, 'action': 'Register'})


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
