from typing import Any
from django.db.models.query import QuerySet
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import ListView, UpdateView, DeleteView

from .models import Task
from .forms import CreateTaskForm, UpdateTaskForm


class TaskListView(ListView):
    model = Task
    template_name = "todos/task_list.html"
    context_object_name = "tasks"

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def post(self, request):
        if request.method == 'POST':
            form = CreateTaskForm(request.POST)
            if form.is_valid():
                task = form.save(commit=False)
                task.user = request.user
                task.save()
        return redirect('tasks:task_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_form'] = CreateTaskForm()
        return context


class TaskDetailView(DeleteView):
    model = Task
    template_name = "todos/task_detail.html"
    context_object_name = "task"

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)


class TaskUpdateView(UpdateView):
    model = Task
    form_class = UpdateTaskForm
    template_name = "todos/task_update.html"
    success_url = '/task'

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    
    def get_object(self, queryset=None):
        return Task.objects.get(pk=self.kwargs['pk'])


class TaskDeleteView(DeleteView):
    model = Task
    template_name = "todos/task_confirm_delete.html"
    success_url = reverse_lazy('tasks:task_list')

