"""
URL configuration for MatrizEisenhower project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
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
    path('update-task-priority/', login_required(task_views.update_task_priority), name='update_task_priority'),
    path('audit-log/', login_required(task_views.audit_log_view), name='audit_log'),
]
