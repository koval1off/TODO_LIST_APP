from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, UpdateView, DeleteView, DetailView
from django.http import JsonResponse
from django.views import View
from django.shortcuts import get_object_or_404

from .models import Task
from .forms import UpdateTaskForm
from .mixins import TaskListViewMixin
    

class TaskListView(TaskListViewMixin, ListView):
    context_object_name = "tasks"
    
    def get_redirect_url(self):
        return reverse('tasks:task_list')
    

class ToggleTaskCompletionView(View):
    def post(self, request, task_id):
        task = get_object_or_404(Task, id=task_id, user=request.user)
        task.completed = not task.completed
        task.save()
        return JsonResponse({'success': True})


class TaskDetailView(DetailView):
    model = Task
    template_name = "todos/task_detail.html"
    context_object_name = "task"

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)


class TaskUpdateView(UpdateView):
    model = Task
    form_class = UpdateTaskForm
    template_name = "todos/task_update.html"

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    
    def get_object(self, queryset=None):
        return Task.objects.get(pk=self.kwargs['pk'])
    
    def get_success_url(self):
        return self.object.get_absolute_url()


class TaskDeleteView(DeleteView):
    model = Task
    template_name = "todos/task_confirm_delete.html"
    success_url = reverse_lazy('tasks:task_list')

