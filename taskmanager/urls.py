# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.matrix_view, name='matrix'),
    path('create-task/', views.create_task_view, name='create_task'),
    path('update-task/<int:task_id>/', views.update_task_view, name='update_task'),
    path('delete-task/<int:task_id>/', views.delete_task_view, name='delete_task'),
    path('update-task-priority/', views.update_task_priority, name='update_task_priority'),
    path('mark-completed/<int:task_id>/', views.mark_completed, name='mark_completed'),
    path('audit-log/', views.audit_log_view, name='audit_log'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('reportes/', views.reportes_tareas, name='reportes'),  # Nueva URL para el reporte
    path('gantt-vencidas/', views.gantt_tareas_vencidas, name='gantt_tareas_vencidas'),
]
