from rest_framework import serializers
from todos.models import Task
from groups.models import TaskGroup


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["id", "user", "title", "description", "completed"]


class TaskGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskGroup
        fields = ["id", "name", "members"]

        