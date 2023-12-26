from django.contrib.auth.models import User


def find_user_by_id(user_id):
    """Find a User by its ID."""
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return None

    return user
