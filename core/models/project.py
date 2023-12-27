from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    creator = models.ForeignKey('User', on_delete=models.CASCADE)
    members = models.ManyToManyField('User', related_name='projects')
    modified = models.DateTimeField(auto_now=True)
