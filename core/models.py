from django.db import models


class Task(models.Model):
    title = models.CharField(max_length=200)
    type = models.ForeignKey('Type', on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    status = models.ForeignKey('Status', on_delete=models.CASCADE)
    resolution = models.ForeignKey('Resolution', on_delete=models.CASCADE, blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    assignee = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='assignee', blank=True, null=True)
    creator = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='reporter')
    modified = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Status(models.Model):
    status = models.CharField(max_length=200)

    def __str__(self):
        return self.status


class Type(models.Model):
    type = models.CharField(max_length=200)

    def __str__(self):
        return self.type


class Resolution(models.Model):
    resolution = models.CharField(max_length=200)

    def __str__(self):
        return self.resolution