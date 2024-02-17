from rest_framework_api_key.permissions import HasAPIKey


class TaskGuruHasAPIKey(HasAPIKey):
    def has_permission(self, request, view):
        if request.META.get('HTTP_ORIGIN', '') == 'http://localhost:8000':
            return True
        elif request.META.get('PATH_INFO', '') == '/api/github/proxy':
            return True
        elif request.META.get('PATH_INFO', '') == '/api/api-key':
            return True
        else:
            return super().has_permission(request, view)
