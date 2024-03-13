from django.urls import path
from .views import TaskListAPIView, TaskDetailAPIView, TaskGroupAPIView


urlpatterns = [
    path('groups/', TaskGroupAPIView.as_view(), name='group_list_api'),
    path('tasks/', TaskListAPIView.as_view(), name='task_list_api'),
    path('tasks/<uuid:pk>/', TaskDetailAPIView.as_view(), name='task_detail_api'),
]
