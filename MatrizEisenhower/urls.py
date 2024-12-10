from django.contrib import admin
from django.urls import path
from django.contrib.auth.decorators import login_required
from taskmanager import views as task_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/login/'), name='logout'),
    path('', login_required(task_views.matrix_view), name='matrix'),
    path('create-task/', login_required(task_views.create_task_view), name='create_task'),
    path('update-task/<int:task_id>/', login_required(task_views.update_task_view), name='update_task'),
    path('delete-task/<int:task_id>/', login_required(task_views.delete_task_view), name='delete_task'),
    path('audit-log/', login_required(task_views.audit_log_view), name='audit_log'),
]
