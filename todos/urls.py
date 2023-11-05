from django.urls import path

from .views import (
    TaskListView,
    TaskDetailView,
    TaskCreateView,
    TaskUpdateView,
    TaskDeleteView,
)

app_name = "tasks"

urlpatterns = [
    path('', TaskListView.as_view(), name='task_list'),
    path('task/<int:pk>/', TaskDetailView.as_view(), name='task_detail'),
    path('task/edit/<int:pk>/', TaskUpdateView.as_view(), name='task_update'),
    path('task/delete/<int:pk>/', TaskDeleteView.as_view(), name='task_delete'),
]