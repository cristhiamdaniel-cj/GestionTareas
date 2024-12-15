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
from django.db import transaction  # Importar transaction


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

@login_required
def create_task_view(request):
    print(f"==> Entrando a create_task_view - Usuario: {request.user.username}")
    if request.method == 'POST':
        print("Datos recibidos en POST:", request.POST)
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)  # No guarda aún en la base de datos
            task.assigned_to = form.cleaned_data['assigned_to']  # Asigna el valor correcto
            task.save()
            print(f"Tarea creada: {task}")
            # Crear un registro en la auditoría
            AuditLog.objects.create(
                user=request.user,
                action='create',
                task=task,
                timestamp=now(),
                description=f"Tarea creada: {task.title}, Asignado a: {task.assigned_to}"
            )
            return redirect('matrix')
        else:
            print("Errores del formulario:", form.errors)
    else:
        form = TaskForm()
    return render(request, 'create_task.html', {'form': form})



# Vista para actualizar una tarea
@login_required
def update_task_view(request, task_id):
    print(f"==> Entrando a update_task_view - Usuario: {request.user.username} - Tarea ID: {task_id}")
    task = get_object_or_404(Task, id=task_id)
    print(f"Tarea encontrada: {task}")

    old_values = {field.name: getattr(task, field.name) for field in task._meta.fields}  # Capturar valores antiguos

    if request.method == 'POST':
        print("Datos recibidos en POST:", request.POST)
        form = TaskForm(request.POST, instance=task)
        print("Errores del formulario antes de validar:", form.errors)

        if form.is_valid():
            form.save()
            changes = [
                f"{field}: '{old_value}' → '{getattr(task, field)}'"
                for field, old_value in old_values.items()
                if old_value != getattr(task, field)
            ]
            print(f"Tarea actualizada: {task}")
            # Registrar los cambios en la auditoría
            AuditLog.objects.create(
                user=request.user,
                action="update",
                task=task,
                timestamp=now(),
                description=f"Tarea actualizada: {', '.join(changes)}" if changes else "No se realizaron cambios"
            )
            return redirect('matrix')
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
        # Registrar en la auditoría antes de eliminar
        AuditLog.objects.create(
            user=request.user,
            action="delete",
            task=task,
            timestamp=now(),
            description=f"Tarea eliminada: {task.title}"
        )
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
        try:
            # Iniciar una transacción para mayor seguridad
            with transaction.atomic():
                data = json.loads(request.body)
                print("Datos recibidos en JSON:", data)

                task_id = data.get("task_id")
                new_priority = data.get("new_priority")

                if not task_id or not new_priority:
                    return JsonResponse({"status": "error", "message": "Datos incompletos"}, status=400)

                task = get_object_or_404(Task, id=task_id)
                old_priority = task.priority

                # Verificar si la prioridad realmente cambió
                if old_priority != new_priority:
                    task.priority = new_priority
                    task.save()

                    # Registrar el cambio en AuditLog
                    AuditLog.objects.create(
                        user=request.user,
                        action="update",
                        task=task,
                        timestamp=now(),
                        description=f"Prioridad actualizada de '{old_priority}' → '{new_priority}'"
                    )
                    print(f"Registro de auditoría creado para la tarea {task.title}")

                return JsonResponse({"status": "success", "message": "Prioridad actualizada"})

        except Exception as e:
            print(f"Error inesperado: {e}")
            return JsonResponse({"status": "error", "message": "Error interno del servidor"}, status=500)

    return JsonResponse({"status": "error", "message": "Método no permitido"}, status=405)


# Vista para cambiar el estado de una tarea
@login_required
def mark_completed(request, task_id):
    print(f"==> Entrando a mark_completed - Usuario: {request.user.username} - Tarea ID: {task_id}")
    task = get_object_or_404(Task, id=task_id)
    old_status = task.status  # Estado anterior
    
    # Cambiar estado de la tarea
    task.status = 'completed' if task.status == 'in_progress' else 'in_progress'
    task.save()
    new_status = task.status  # Nuevo estado
    print(f"Estado de la tarea {task.title} cambiado a: {task.get_status_display()}")

    # Registrar en la auditoría
    try:
        audit_log = AuditLog.objects.create(
            user=request.user,
            action="update",
            task=task,
            timestamp=now(),
            description=f"Estado cambiado de '{old_status}' → '{new_status}'"
        )
        print(f"Registro de auditoría creado: {audit_log}")
    except Exception as e:
        print(f"Error al crear el registro de auditoría: {e}")

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
