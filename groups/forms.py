from django import forms
from .models import TaskGroup


class CreateGroupForm(forms.ModelForm):
    class Meta:
        model = TaskGroup
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'my text here'}),
        }
    name = forms.CharField(label='', required=True)
