from django.contrib import admin
from django.urls import path, include  # Incluye 'include'
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from taskmanager import views as task_views  # Importa las vistas de taskmanager

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/login/'), name='logout'),
    path('', login_required(task_views.matrix_view), name='matrix'),  # Usa 'task_views'
    path('taskmanager/', include('taskmanager.urls')),  # Incluye las URLs de taskmanager
]
