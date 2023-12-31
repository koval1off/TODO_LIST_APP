from typing import Any
from django.db.models.query import QuerySet
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect
from django.views.generic import ListView, UpdateView, DeleteView
from django.http import JsonResponse
from django.views import View
from django.shortcuts import get_object_or_404

from .models import Task
from groups.models import TaskGroup
from .forms import CreateTaskForm, UpdateTaskForm


class GroupTaskListView(ListView):
    model = Task
    template_name = "todos/task_list.html"
    context_object_name = "group_tasks"
    form_class = CreateTaskForm

    def get_queryset(self):
        user = self.request.user
        group_id = self.kwargs.get("group_id")
        return Task.objects.filter(group_id=group_id, user=user)
    
    def post(self, request, *args, **kwargs):
        group_id = self.kwargs.get("group_id")
        form = self.form_class(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.group = get_object_or_404(TaskGroup, id=group_id)
            task.save()
        
        task_ids = request.POST.getlist("task_ids")
        if task_ids:
            Task.objects.filter(id__in=task_ids, user=request.user).update(completed=True)
        
        return redirect(reverse("tasks:group_task_list", args=[group_id]))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        group_id = self.kwargs.get("group_id")
        context["incompleted_tasks"] = self.get_queryset().filter(completed=False)
        context["completed_tasks"] = self.get_queryset().filter(completed=True)
        context["create_form"] = self.form_class(initial={'group': group_id})
        context["group_id"] = group_id
        return context
    

class TaskListView(ListView):
    model = Task
    template_name = "todos/task_list.html"
    context_object_name = "tasks"
    form_class = CreateTaskForm

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(user=user)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()

        task_ids = request.POST.getlist('task_ids')
        if task_ids:
            Task.objects.filter(id__in=task_ids, user=request.user).update(completed=True)

        return redirect(reverse('tasks:task_list'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['incompleted_tasks'] = Task.objects.filter(completed=False)
        context['completed_tasks'] = Task.objects.filter(completed=True)
        context['create_form'] = self.form_class()
        return context


class ToggleTaskCompletionView(View):
    def post(self, request, task_id):
        task = get_object_or_404(Task, id=task_id, user=request.user)
        task.completed = not task.completed
        task.save()
        return JsonResponse({'success': True})


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

