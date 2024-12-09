from django.urls import path
from . import views

urlpatterns = [
    path('', views.matrix_view, name='matrix'),
    path('create-task/', views.create_task_view, name='create_task'),
    path('update-task/<int:task_id>/', views.update_task_view, name='update_task'),
    path('delete-task/<int:task_id>/', views.delete_task_view, name='delete_task'),
    path('update-task-priority/', views.update_task_priority, name='update_task_priority'),
    path('audit-log/', views.audit_log_view, name='audit_log'),
]
