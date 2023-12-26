from django.db import models


class TaskGuruUser(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'TaskGuruUsers'
