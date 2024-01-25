from django.urls import path

from .views import (
    TaskListView,
    TaskDetailView,
    TaskUpdateView,
    TaskDeleteView,
    ToggleTaskCompletionView,
)

app_name = "tasks"

urlpatterns = [
    path('', TaskListView.as_view(), name='task_list'),
    path('<uuid:pk>/', TaskDetailView.as_view(), name='task_detail'),
    path('<uuid:pk>/update', TaskUpdateView.as_view(), name='task_update'),
    path('<uuid:pk>/detele', TaskDeleteView.as_view(), name='task_delete'),
    path('toggle-completion/<uuid:task_id>/', ToggleTaskCompletionView.as_view(), name='toggle_task_completion'),
]
