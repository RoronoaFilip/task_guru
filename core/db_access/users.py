from core.models.user import TaskGuruUser


def find_user_by_id(user_id):
    """Find a User by its ID."""
    try:
        user = TaskGuruUser.objects.get(id=user_id)
    except TaskGuruUser.DoesNotExist:
        return None

    return user
