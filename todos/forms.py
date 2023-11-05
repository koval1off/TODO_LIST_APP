from django import forms

from .models import Task


class CreateTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title']


class UpdateTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'completed']
        