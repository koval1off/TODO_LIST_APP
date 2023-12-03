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
    path('group/<int:group_id>/', TaskListView.as_view(), name='task_list_by_group'),
    path('<int:pk>/', TaskDetailView.as_view(), name='task_detail'),
    path('edit/<int:pk>/', TaskUpdateView.as_view(), name='task_update'),
    path('delete/<int:pk>/', TaskDeleteView.as_view(), name='task_delete'),
    path('toggle-completion/<int:task_id>/', ToggleTaskCompletionView.as_view(), name='toggle_task_completion'),
]