from django.urls import path
from .views import GroupListView


app_name = 'groups'

urlpatterns = [
    path('', GroupListView.as_view(), name='group_list'),
]