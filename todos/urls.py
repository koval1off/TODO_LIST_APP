from django.urls import path

from .views import TaskListView, TaskCreateView


urlpatterns = [
    path('', TaskListView.as_view(), name='task-list'),
    path('add/', TaskCreateView.as_view(), name='task-create'),
]