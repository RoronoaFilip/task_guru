from rest_framework import status
from rest_framework.response import Response


def accept_json(view_func):
    """Decorator to only accept requests with content type JSON."""

    def wrapper(*args, **kwargs):
        request = args[0]
        if request.content_type != 'application/json':
            return Response({
                'error': 'Content-Type must be application/json'
            }, status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
        return view_func(*args, **kwargs)

    return wrapper


def content_type_json(view_func):
    """Decorator to set the content type to JSON."""

    def wrapper(*args, **kwargs):
        response = view_func(*args, **kwargs)
        response['Content-Type'] = 'application/json'
        return response

    return wrapper
