from django.db import models


class Task(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    type = models.ForeignKey('Type', on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    status = models.ForeignKey('Status', on_delete=models.CASCADE)
    resolution = models.ForeignKey('Resolution', on_delete=models.CASCADE, blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    assignee = models.ForeignKey('TaskGuruUser', on_delete=models.CASCADE, related_name='assignee', blank=True, null=True)
    creator = models.ForeignKey('TaskGuruUser', on_delete=models.CASCADE, related_name='reporter')
    modified = models.DateTimeField(auto_now_add=True)

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


class Resolution(models.Model):
    id = models.AutoField(primary_key=True)
    resolution = models.CharField(max_length=200)

    def __str__(self):
        return self.resolution
