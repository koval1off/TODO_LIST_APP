from django.views.generic import ListView
from django.shortcuts import redirect
from .models import TaskGroup
from .forms import CreateGroupForm


class GroupListView(ListView):
    model = TaskGroup
    template_name = "groups/group_list.html"
    context_object_name = "groups"

    def get_queryset(self):
        return TaskGroup.objects.filter(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["create_form"] = CreateGroupForm()
        return context
    
    def post(self, request, *args, **kwargs):
        if request.method == "POST":
            form = CreateGroupForm(request.POST)
            if form.is_valid():
                new_group = form.save(commit=False)
                new_group.user = request.user
                new_group.save()
        return redirect("groups:group_list")

    
