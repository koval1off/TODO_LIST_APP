from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from groups.models import TaskGroup
import uuid


class Task(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(TaskGroup, on_delete=models.CASCADE, related_name='tasks', null=True, default=None)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    completed = models.BooleanField(default=False, null=True)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("tasks:task_detail", args=[str(self.id)])
    
