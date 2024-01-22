from django.urls import path
from django.conf.urls import handler404, handler500

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

handler404 = 'todos.views.my_custom_page_not_found_view'
handler500 = 'todos.views.my_custom_error_view'
