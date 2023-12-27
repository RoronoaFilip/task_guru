from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    creator = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    members = models.ManyToManyField('auth.User', related_name='projects')
