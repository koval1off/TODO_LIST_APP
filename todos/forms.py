from django import forms

from .models import Task


class CreateTaskForm(forms.ModelForm):
    title = forms.CharField(
        label='',
        required=True,
        widget=forms.TextInput(attrs={'placeholder':'Add new task..'})
    )

    class Meta:
        model = Task
        fields = ['title']


class UpdateTaskForm(forms.ModelForm):
    completed = forms.BooleanField(
        label='Completed',
        required=False,
        widget=forms.CheckboxInput()
    )

    class Meta:
        model = Task
        fields = ['title', 'description', 'completed']
        
