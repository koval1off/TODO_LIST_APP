from django.views.generic import ListView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.db import transaction

from todos.models import Task
from todos.mixins import TaskListViewMixin
from .models import TaskGroup, Invitation
from .forms import CreateGroupForm, UpdateGroupForm
from .utils import create_invitation, get_invitation_link


class GroupListView(LoginRequiredMixin, ListView):
    model = TaskGroup
    template_name = "groups/group_list.html"
    context_object_name = "groups"

    def get_queryset(self):
        return TaskGroup.objects.filter(members=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["create_form"] = CreateGroupForm()
        return context
    
    def post(self, request, *args, **kwargs):
        form = CreateGroupForm(request.POST)
        if form.is_valid():
            new_group = form.save(commit=False)
            with transaction.atomic():       
                new_group.save()
                new_group.members.add(request.user)
        return redirect("groups:group_list")

    
class GroupTaskListView(TaskListViewMixin, ListView):
    context_object_name = "group_tasks"

    def get_queryset(self):
        group_id = self.kwargs.get("group_id")
        group = get_object_or_404(TaskGroup, id=group_id)
        return Task.objects.filter(group=group)
    
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
        
        return redirect(self.get_redirect_url())
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        group_id = self.kwargs.get("group_id")
        group = get_object_or_404(TaskGroup, id=group_id)
        context["create_form"] = self.form_class(initial={'group': group_id})
        context["group_id"] = group_id
        context["group"] = group
        return context
    
    def get_redirect_url(self):
        group_id = self.kwargs.get("group_id")
        return reverse("groups:group_task_list", args=[group_id])
    

class GroupUpdateView(LoginRequiredMixin, UpdateView):
    model = TaskGroup
    template_name = "groups/group_update.html"
    form_class = UpdateGroupForm
    success_url = "/group"

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    
    def get_object(self, queryset=None):
        group_id = self.kwargs.get('group_id')
        return get_object_or_404(TaskGroup, id=group_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        group_id = self.kwargs.get('group_id')
        context['group_id'] = group_id

        invitation = create_invitation(self.request, group_id)
        invitation_link = get_invitation_link(self.request, invitation)
        context["invitation_link"] = invitation_link

        return context


class GroupDeteleView(LoginRequiredMixin, DeleteView):
    model = TaskGroup
    template_name = "groups/group_confirm_delete.html"
    success_url = reverse_lazy("groups:group_list")

    def get_object(self, queryset=None):
        group_id = self.kwargs.get('group_id')
        return get_object_or_404(TaskGroup, id=group_id)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        group_id = self.kwargs.get("group_id")
        group = get_object_or_404(TaskGroup, id=group_id)
        context['group_id'] = group_id
        context['group'] = group
        return context


def accept_invitation(request, token):
    if request.user.is_authenticated:
        invitation = get_object_or_404(Invitation, token=token)
        invitation.group.members.add(request.user)
        invitation.save()
        return redirect("groups:group_task_list", group_id=invitation.group.id)
    else:
        request.session["invitation_token"] = str(token)
        return redirect("account_login")
    