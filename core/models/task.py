from django.db import models


class Task(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    type = models.ForeignKey('Type', on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    status = models.ForeignKey('Status', on_delete=models.CASCADE)
    assignee = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='assignee', blank=True, null=True)
    creator = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='reporter')
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='tasks')

    def __str__(self):
        return self.title


class Status(models.Model):
    id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=200)

    def __str__(self):
        return self.status

    class Meta:
        db_table = 'Statuses'


class Type(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=200)

    def __str__(self):
        return self.type
