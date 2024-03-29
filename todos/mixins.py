from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect

from .models import Task
from .forms import CreateTaskForm


class TaskListViewMixin(LoginRequiredMixin):
    model = Task
    template_name = "todos/task_list.html"
    form_class = CreateTaskForm

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(user=user).order_by("-created_at").prefetch_related("user")
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()

        task_ids = request.POST.getlist('task_ids')
        if task_ids:
            Task.objects.filter(id__in=task, user=request.user).update(completed=True)
        
        return redirect(self.get_redirect_url())
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['incompleted_tasks'] = self.get_queryset().filter(completed=False)
        context['completed_tasks'] = self.get_queryset().filter(completed=True)
        context['create_form'] = self.form_class()
        return context
    
    def get_redirect_url(self):
        raise NotImplementedError("Subclasses must impletement this method.")
    
