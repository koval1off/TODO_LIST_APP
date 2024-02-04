from django.urls import path
from .views import (
    GroupListView, 
    GroupTaskListView, 
    GroupDeteleView, 
    GroupUpdateView,
    accept_invitation,
)

app_name = 'groups'

urlpatterns = [
    path('', GroupListView.as_view(), name='group_list'),
    path('<uuid:group_id>/tasks', GroupTaskListView.as_view(), name='group_task_list'),
    path('<uuid:group_id>/update', GroupUpdateView.as_view(), name='group_update'),
    path('<uuid:group_id>/delete', GroupDeteleView.as_view(), name='group_delete'),
    path('<uuid:token>/accept-invitation', accept_invitation, name='accept_invitation'),
]
