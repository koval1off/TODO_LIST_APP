from django.contrib import admin
from .models import TaskGroup


@admin.register(TaskGroup)
class GroupAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "user")
    list_filter = ("name",)