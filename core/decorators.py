from django.contrib.auth.models import User
from django.http import HttpRequest
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response

from core.models.log import Log


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


def log(view_func):
    """Decorator to log requests and responses."""

    def wrapper(*args, **kwargs):
        request = args[0]  # request is always the first argument
        if not isinstance(request, HttpRequest):
            request = args[1]

        data = ''
        if isinstance(request, Request):
            data = request.data

        try:
            user = User.objects.filter(id=request.user.id).first()
        except User.DoesNotExist:
            user = None

        request_log = Log(
            user=user,
            request_method=request.method,
            request_uri=request.path,
            payload=data,
        )
        response = view_func(*args, **kwargs)
        request_log.response_status = response.status_code or None
        request_log.save()
        return response

    return wrapper


def except_and_then(class_to_except, then):
    """Return a decorator that catches the given exception and returns the given function."""
    def decorator(view_func):
        def wrapper(*args, **kwargs):
            try:
                return view_func(*args, **kwargs)
            except class_to_except:
                return then()
        return wrapper
    return decorator

