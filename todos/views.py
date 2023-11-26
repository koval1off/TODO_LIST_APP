from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import ListView, UpdateView, DeleteView
from django.http import JsonResponse
from django.views import View
from django.shortcuts import get_object_or_404

from .models import Task
from .forms import CreateTaskForm, UpdateTaskForm


class TaskListView(ListView):
    model = Task
    template_name = "todos/task_list.html"
    context_object_name = "tasks"

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user, completed=False)

    def post(self, request):
        if request.method == 'POST':
            form = CreateTaskForm(request.POST)
            if form.is_valid():
                task = form.save(commit=False)
                task.user = request.user
                task.save()

            task_ids = request.POST.getlist('task_ids')
            if task_ids:
                Task.objects.filter(id__in=task_ids).update(is_completed=True)

        return redirect('tasks:task_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['completed_tasks'] = Task.objects.filter(user=self.request.user, completed=True)
        context['create_form'] = CreateTaskForm()
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



