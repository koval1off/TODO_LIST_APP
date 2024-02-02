from django.contrib import admin
from .models import TaskGroup


@admin.register(TaskGroup)
class GroupAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "display_members")
    list_filter = ("name",)
    
    def display_members(self, obj):
        return ", ".join([members.username for members in obj.members.all()])
    
    display_members.short_description = "Members"
    