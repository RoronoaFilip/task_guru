import requests
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from core.decorators import content_type_json, log, except_and_then
from task_guru.settings import GITHUB_TOKEN


class GithubRequestException(Exception):
    """Exception for github request errors."""
    pass


EXCEPTION = GithubRequestException


def and_then_callback():
    """Called after the exception is caught."""
    return Response(status=status.HTTP_400_BAD_REQUEST)


@log
@content_type_json
@except_and_then(EXCEPTION, and_then_callback)
@api_view(['GET'])
def github_proxy(request):
    """Proxy for github requests."""
    url = request.GET.get('url')

    if url is None:
        raise GithubRequestException()

    response = requests.get(url, headers={
        'Authorization': f'Bearer {GITHUB_TOKEN}'
    })

    if response.status_code != 200:
        raise GithubRequestException()

    return Response(status=status.HTTP_200_OK, data=response.json())
