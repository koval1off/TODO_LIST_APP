from django import forms
from .models import TaskGroup


class CreateGroupForm(forms.ModelForm):
    name = forms.CharField(
        label='',
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Add new group..'})
    )

    class Meta:
        model = TaskGroup
        fields = ['name']


class UpdateGroupForm(forms.ModelForm):
    class Meta:
        model = TaskGroup
        fields = ['name']