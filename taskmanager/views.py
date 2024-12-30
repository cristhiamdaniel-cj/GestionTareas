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
from .forms import SolutionForm  # Importar el formulario
from django.contrib.auth.decorators import user_passes_test, login_required
from django.shortcuts import redirect
from django.shortcuts import render
from django.utils import timezone


def gantt_tareas_vencidas(request):
    """
    Vista que prepara datos de tareas vencidas para mostrar en un diagrama de Gantt.
    """
    tareas_vencidas = Task.objects.filter(due_date__lt=timezone.now(), status='in_progress')

    # Crear un diccionario de datos con título y fechas
    datos_tareas = [
        {
            'title': tarea.title,
            'start_date': tarea.start_date.strftime('%Y-%m-%d'),
            'due_date': tarea.due_date.strftime('%Y-%m-%d'),
        }
        for tarea in tareas_vencidas
    ]

    return render(request, 'gantt_tareas_vencidas.html', {'datos_tareas': datos_tareas})



def reportes_tareas(request):
    """
    Vista para mostrar un reporte de tareas:
    - Total de tareas
    - Tareas completadas
    - Tareas activas
    - Tareas asignadas
    - Tareas vencidas
    """
    total_tareas = Task.objects.count()
    tareas_completadas = Task.objects.filter(status='completed').count()
    tareas_activas = Task.objects.filter(status='in_progress').count()
    tareas_asignadas = Task.objects.exclude(assigned_to='Sin asignar').count()
    tareas_vencidas = Task.objects.filter(due_date__lt=timezone.now(), status='in_progress')

    context = {
        'total_tareas': total_tareas,
        'tareas_completadas': tareas_completadas,
        'tareas_activas': tareas_activas,
        'tareas_asignadas': tareas_asignadas,
        'tareas_vencidas': tareas_vencidas
    }

    return render(request, 'reportes.html', context)


# Función que verifica si el usuario es superusuario
def is_superuser(user):
    return user.is_superuser

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
            task = form.save(commit=False)  # Guardar sin realizar el commit
            task.assigned_to = form.cleaned_data['assigned_to']  # Asignar 'assigned_to'
            task.save()

            # Registrar la creación en el AuditLog
            assigned_to_text = task.assigned_to if task.assigned_to else "Sin asignar"
            AuditLog.objects.create(
                user=request.user,
                action='create',
                task=task,
                description=f"Tarea creada: {task.title}, Asignado a: {assigned_to_text}"
            )
            print(f"Tarea creada: {task}")
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
    task = get_object_or_404(Task, id=task_id)  # Obtener la tarea actual
    print(f"Tarea encontrada: {task}")

    old_values = {field.name: getattr(task, field.name) for field in task._meta.fields}  # Capturar valores antiguos para auditoría

    if request.method == 'POST':
        print("Datos recibidos en POST:", request.POST)
        form = TaskForm(request.POST, instance=task)  # Pasar la instancia de la tarea al formulario
        print("Errores del formulario antes de validar:", form.errors)

        if form.is_valid():
            updated_task = form.save(commit=False)  # Guardar sin commit
            updated_task.assigned_to = form.cleaned_data.get('assigned_to')  # Asegurar el valor de 'assigned_to'
            updated_task.save()  # Guardar cambios

            # Identificar cambios realizados
            changes = [
                f"{field}: '{old_value}' → '{getattr(task, field)}'"
                for field, old_value in old_values.items()
                if old_value != getattr(task, field)
            ]
            print(f"Tarea actualizada: {task}")

            # Registrar cambios en el log de auditoría
            AuditLog.objects.create(
                user=request.user,
                action="update",
                task=task,
                timestamp=now(),
                description=f"Tarea actualizada: {', '.join(changes)}" if changes else "No se realizaron cambios"
            )
            return redirect('matrix')  # Redirigir a la matriz de Eisenhower
        else:
            print("Errores del formulario después de validar:", form.errors)
    else:
        # Inicializar el formulario con valores actuales
        form = TaskForm(instance=task, initial={
            'assigned_to_predefined': task.assigned_to if task.assigned_to in dict(TaskForm.ASSIGN_TO_CHOICES) else 'Otros',
            'assigned_to_custom': '' if task.assigned_to in dict(TaskForm.ASSIGN_TO_CHOICES) else task.assigned_to,
        })

    return render(request, 'update_task.html', {'form': form, 'task': task})


# Vista para eliminar una tarea
@login_required
@user_passes_test(is_superuser)
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

    if request.method == "POST":
        form = SolutionForm(request.POST)
        if form.is_valid():
            solution = form.cleaned_data['solution']

            # Cambiar el estado de la tarea a 'completed'
            task.status = 'completed' if task.status == 'in_progress' else 'in_progress'
            task.description += f"\n\nSolución: {solution}"  # Agregar solución a la descripción
            task.save()
            new_status = task.status  # Nuevo estado

            # Registrar en la auditoría
            description = f"Estado cambiado de '{old_status}' → '{new_status}'. Solución: {solution}"
            AuditLog.objects.create(
                user=request.user,
                action="update",
                task=task,
                timestamp=now(),
                description=description
            )
            print(f"Tarea {task.title} marcada como completada con solución: {solution}")
            return redirect('matrix')
    else:
        form = SolutionForm()

    return render(request, 'mark_completed.html', {'form': form, 'task': task})



# Vista para ver el registro de auditoría
@login_required
@user_passes_test(is_superuser)
def audit_log_view(request):
    print(f"==> Entrando a audit_log_view - Usuario: {request.user.username}")
    if request.user.username != 'danielcampos':
        print("Acceso denegado a la vista de auditoría")
        return redirect('matrix')
    logs = AuditLog.objects.all()
    print(f"Registros de auditoría cargados: {logs}")
    return render(request, 'audit_log.html', {'logs': logs})
