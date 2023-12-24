from django.urls import path

from .views import (
    GroupTaskListView,
    TaskListView,
    TaskDetailView,
    TaskUpdateView,
    TaskDeleteView,
    ToggleTaskCompletionView,
)

app_name = "tasks"

urlpatterns = [
    path('', TaskListView.as_view(), name='task_list'),
    path('group/<uuid:group_id>/', GroupTaskListView.as_view(), name='group_task_list'),
    path('<uuid:pk>/', TaskDetailView.as_view(), name='task_detail'),
    path('edit/<uuid:pk>/', TaskUpdateView.as_view(), name='task_update'),
    path('delete/<uuid:pk>/', TaskDeleteView.as_view(), name='task_delete'),
    path('toggle-completion/<uuid:task_id>/', ToggleTaskCompletionView.as_view(), name='toggle_task_completion'),
]