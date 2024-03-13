from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from todos.models import Task
from groups.models import TaskGroup
from .serializers import TaskSerializer, TaskGroupSerializer


class TaskListAPIView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TaskDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]


class TaskGroupAPIView(generics.ListCreateAPIView):
    serializer_class = TaskGroupSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return TaskGroup.objects.filter(members=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

