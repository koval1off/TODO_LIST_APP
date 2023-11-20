from django import forms

from .models import Task


class CreateTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'my text here'}),
        }
    title = forms.CharField(label='', required=True)


class UpdateTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'completed']
        