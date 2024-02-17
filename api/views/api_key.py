from datetime import timedelta

from django.contrib.auth import authenticate
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_api_key.models import APIKey


class GenerateAPIKeyView(APIView):
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if user is None:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        _invalidate_user_api_key(user)

        expiration_date = timezone.now() + timedelta(days=30)
        api_key, key = APIKey.objects.create_key(name=user.username, expiry_date=expiration_date)

        return Response({'api_key': key, 'expiration_date': expiration_date}, status=status.HTTP_201_CREATED)


def _invalidate_user_api_key(user):
    """Invalidate the user's API key if present."""
    try:
        api_key = APIKey.objects.get(name=user.username, revoked=False)
        api_key.revoked = True
        api_key.expires = timezone.now()
        api_key.save()
    except APIKey.DoesNotExist:
        pass
