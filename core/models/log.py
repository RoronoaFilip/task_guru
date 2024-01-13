from django.db import models


class Log(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True)
    request_method = models.CharField(max_length=10, null=True)
    request_uri = models.CharField(max_length=100, null=True)
    payload = models.TextField(null=True)
    response_status = models.IntegerField(null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
