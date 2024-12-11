from django.utils.timezone import now
from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    due_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        initial=now
    )

    class Meta:
        model = Task
        fields = [
            'title', 'description', 'assigned_to', 'area', 'subgroup', 
            'role', 'due_date', 'priority', 'status'
        ]
