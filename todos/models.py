from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Task(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    completed = models.BooleanField(default=False, null=True)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("tasks:task_detail", args=[str(self.id)])
    