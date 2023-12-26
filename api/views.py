from datetime import datetime

from core.models import Task


def create_task(request):
    """Create a new Task object from a POST request."""
    task = Task.objects.create(
        title=request.POST['title'],
        type=request.POST['type'],
        description=request.POST['description'],
        status=request.POST['status'],
        resolution=request.POST['resolution'],
        parent=request.POST['parent'],
        assignee=request.POST['assignee'],
        creator=request.POST['creator'],
        modified=datetime.now()
    )
