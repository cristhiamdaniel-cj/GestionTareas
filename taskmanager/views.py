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
    print("==> Entrando a login_view")
    if request.method == 'POST':
        print("Datos recibidos en POST:", request.POST)
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            print(f"Inicio de sesión exitoso para el usuario: {user.username}")
            next_url = request.GET.get('next', '/')
            return redirect(next_url)
        else:
            print(f"Errores de autenticación: {form.errors}")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# Vista de cierre de sesión
@login_required
def custom_logout(request):
    print("==> Entrando a custom_logout para cerrar sesión del usuario:", request.user.username)
    logout(request)
    return HttpResponseRedirect(reverse('login'))

# Vista de la matriz de Eisenhower
@login_required
def matrix_view(request):
    print(f"==> Entrando a matrix_view - Usuario: {request.user.username}")
    tasks = {
        'UI': Task.objects.filter(priority='UI'),
        'NI': Task.objects.filter(priority='NI'),
        'IN': Task.objects.filter(priority='IN'),
        'NN': Task.objects.filter(priority='NN'),
    }
    print(f"Tareas cargadas: {tasks}")
    return render(request, 'matrix.html', {'tasks': tasks})

# Vista para crear una tarea
@login_required
def create_task_view(request):
    print(f"==> Entrando a create_task_view - Usuario: {request.user.username}")
    if request.method == 'POST':
        print("Datos recibidos en POST:", request.POST)
        form = TaskForm(request.POST)
        print("Errores del formulario antes de validar:", form.errors)
        if form.is_valid():
            task = form.save()
            print(f"Tarea creada: {task}")
            AuditLog.objects.create(
                user=request.user,
                action='create',
                task=task,
                timestamp=now(),
                description=f"Tarea creada: {task.title}"
            )
            return redirect('matrix')
        else:
            print("Errores del formulario después de validar:", form.errors)
    else:
        form = TaskForm()
    return render(request, 'create_task.html', {'form': form})

# Vista para actualizar una tarea
@login_required
def update_task_view(request, task_id):
    print(f"==> Entrando a update_task_view - Usuario: {request.user.username} - Tarea ID: {task_id}")
    task = get_object_or_404(Task, id=task_id)
    print(f"Tarea encontrada: {task}")
    if request.method == 'POST':
        print("Datos recibidos en POST:", request.POST)
        form = TaskForm(request.POST, instance=task)
        print("Errores del formulario antes de validar:", form.errors)
        if form.is_valid():
            form.save()
            print(f"Tarea actualizada: {task}")
        else:
            print("Errores del formulario después de validar:", form.errors)
    else:
        form = TaskForm(instance=task)
    return render(request, 'update_task.html', {'form': form, 'task': task})

# Vista para eliminar una tarea
@login_required
def delete_task_view(request, task_id):
    print(f"==> Entrando a delete_task_view - Usuario: {request.user.username} - Tarea ID: {task_id}")
    task = get_object_or_404(Task, id=task_id)
    print(f"Tarea encontrada para eliminar: {task}")
    if request.method == 'POST':
        task.delete()
        print(f"Tarea eliminada: {task.title}")
        return redirect('matrix')
    return render(request, 'delete_task.html', {'task': task})

# Vista para actualizar la prioridad de una tarea (arrastrar y soltar)
@csrf_exempt
@login_required
def update_task_priority(request):
    print(f"==> Entrando a update_task_priority - Usuario: {request.user.username}")
    if request.method == "POST":
        data = json.loads(request.body)
        print("Datos recibidos en JSON:", data)
        task_id = data.get("task_id")
        new_priority = data.get("new_priority")
        try:
            task = Task.objects.get(id=task_id)
            print(f"Tarea encontrada: {task}")
            task.priority = new_priority
            task.save()
            print(f"Prioridad actualizada para la tarea {task.title}: {new_priority}")
            return JsonResponse({"status": "success", "message": "Prioridad actualizada"})
        except Task.DoesNotExist:
            print("Error: Tarea no encontrada")
            return JsonResponse({"status": "error", "message": "Tarea no encontrada"}, status=404)

# Vista para cambiar el estado de una tarea
@login_required
def mark_completed(request, task_id):
    print(f"==> Entrando a mark_completed - Usuario: {request.user.username} - Tarea ID: {task_id}")
    task = get_object_or_404(Task, id=task_id)
    task.status = 'completed' if task.status == 'in_progress' else 'in_progress'
    task.save()
    print(f"Estado de la tarea {task.title} cambiado a: {task.get_status_display()}")
    return redirect('matrix')

# Vista para ver el registro de auditoría
@login_required
def audit_log_view(request):
    print(f"==> Entrando a audit_log_view - Usuario: {request.user.username}")
    if request.user.username != 'danielcampos':
        print("Acceso denegado a la vista de auditoría")
        return redirect('matrix')
    logs = AuditLog.objects.all()
    print(f"Registros de auditoría cargados: {logs}")
    return render(request, 'audit_log.html', {'logs': logs})
