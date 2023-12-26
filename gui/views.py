from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required(login_url='/login')
def index(request):
    """Welcome page."""
    return render(request, 'sockets_index.html', {
        'group_name': 'test',
    })
