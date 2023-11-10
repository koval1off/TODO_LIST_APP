from django.urls import path
from .views import TaskListAPIView, TaskDetailAPIView


urlpatterns = [
    path('tasks/', TaskListAPIView.as_view(), name='task_list_api'),
    path('tasks/<int:pk>/', TaskDetailAPIView.as_view(), name='task_detail_api'),
]
