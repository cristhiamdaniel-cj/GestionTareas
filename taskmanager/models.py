from django.db import models
from django.contrib.auth.models import User

from django.db import models

class Task(models.Model):
    PRIORITY_CHOICES = [
        ('UI', 'Urgente e Importante'),
        ('NI', 'No Importante pero Urgente'),
        ('IN', 'Importante pero No Urgente'),
        ('NN', 'No Importante ni Urgente'),
    ]

    STATUS_CHOICES = [
        ('completed', 'Completado'),
        ('in_progress', 'En Proceso'),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField()
    assigned_to = models.CharField(max_length=100)
    area = models.CharField(max_length=100)
    subgroup = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    start_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    priority = models.CharField(max_length=2, choices=PRIORITY_CHOICES)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='in_progress'
    )

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"


class AuditLog(models.Model):
    ACTION_CHOICES = [
        ('create', 'Created Task'),
        ('update', 'Updated Task'),
        ('delete', 'Deleted Task'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    task = models.ForeignKey(Task, on_delete=models.SET_NULL, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user} - {self.action} - {self.timestamp}"
