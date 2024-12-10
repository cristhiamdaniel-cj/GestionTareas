from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse
from django.http import JsonResponse, HttpResponseRedirect
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt
from .models import Task, AuditLog
from .forms import TaskForm
import json

# Vista de inicio de sesión
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            print(f"Inicio de sesión exitoso para el usuario: {user.username}")
            next_url = request.GET.get('next', '/')
            return redirect(next_url)
        else:
            print(f"Errores de autenticación: {form.errors}")
            return render(request, 'login.html', {'form': form, 'errors': form.errors})
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# Vista de cierre de sesión
@login_required
def custom_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))  # Redirige al login después de cerrar sesión

# Vista de la matriz de Eisenhower
@login_required
def matrix_view(request):
    tasks = {
        'UI': Task.objects.filter(priority='UI'),
        'NI': Task.objects.filter(priority='NI'),
        'IN': Task.objects.filter(priority='IN'),
        'NN': Task.objects.filter(priority='NN'),
    }
    return render(request, 'matrix.html', {'tasks': tasks})

# Vista para crear una tarea
@login_required
def create_task_view(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save()
            AuditLog.objects.create(
                user=request.user,
                action='create',
                task=task,
                timestamp=now(),
                description=f"Tarea creada: {task.title}"
            )
            return redirect('matrix')
        else:
            return render(request, 'create_task.html', {'form': form, 'errors': form.errors})
    else:
        form = TaskForm()
    return render(request, 'create_task.html', {'form': form})

# Vista para actualizar una tarea
@login_required
def update_task_view(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    old_values = {field.name: getattr(task, field.name) for field in task._meta.fields}

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            changes = [
                f"{field}: '{old_value}' → '{getattr(task, field)}'"
                for field, old_value in old_values.items()
                if old_value != getattr(task, field)
            ]
            AuditLog.objects.create(
                user=request.user,
                action="update",
                task=task,
                timestamp=now(),
                description=f"Tarea actualizada: {', '.join(changes)}" if changes else "No se realizaron cambios"
            )
            return redirect('matrix')
    else:
        form = TaskForm(instance=task)

    return render(request, 'update_task.html', {'form': form, 'task': task})

# Vista para eliminar una tarea
@login_required
def delete_task_view(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        AuditLog.objects.create(
            user=request.user,
            action="delete",
            task=task,
            timestamp=now(),
            description=f"Tarea '{task.title}' eliminada"
        )
        task.delete()
        return redirect('matrix')
    return render(request, 'delete_task.html', {'task': task})

# Vista para actualizar la prioridad de una tarea (arrastrar y soltar)
@csrf_exempt
@login_required
def update_task_priority(request):
    if request.method == "POST":
        data = json.loads(request.body)
        task_id = data.get("task_id")
        new_priority = data.get("new_priority")

        try:
            task = Task.objects.get(id=task_id)
            old_priority = task.priority
            task.priority = new_priority
            task.save()
            AuditLog.objects.create(
                user=request.user,
                action="update",
                task=task,
                timestamp=now(),
                description=f"Prioridad cambiada de {old_priority} a {new_priority}"
            )
            return JsonResponse({"status": "success", "message": "Prioridad actualizada"})
        except Task.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Tarea no encontrada"}, status=404)

# Vista para ver el registro de auditoría
@login_required
def audit_log_view(request):
    if request.user.username != 'danielcampos':  # Reemplaza con el superusuario esperado
        return redirect('matrix')
    logs = AuditLog.objects.all()
    return render(request, 'audit_log.html', {'logs': logs})
