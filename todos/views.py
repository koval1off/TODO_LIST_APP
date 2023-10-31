from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .models import Task


class TaskListView(ListView):
    model = Task
    template_name = "task_list.html"


class TaskCreateView(CreateView):
    model = Task
    template_name = "task_create.html"
    fields = ['title', 'discription', 'completed']
