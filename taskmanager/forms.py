from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    ASSIGN_TO_CHOICES = [
        ('', '--- Seleccionar ---'),  # Opción en blanco por defecto
        ('Daniela', 'Daniela'),
        ('Sofia', 'Sofia'),
        ('Karla', 'Karla'),
        ('Daniel', 'Daniel'),
        ('Otros', 'Otros'),
        ('Sin asignar', 'Sin asignar'),
    ]

    STATUS_CHOICES = [
        ('', 'Todos'),
        ('in_progress', 'in_progress'),
        ('completed', 'completed'),
        ('Otros', 'Otros'),
    ]

    # Campos de "Asignado a"
    assigned_to_predefined = forms.ChoiceField(
        choices=ASSIGN_TO_CHOICES,
        required=False,
        label="Asignado a",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    assigned_to_custom = forms.CharField(
        required=False,
        label="Nombre Personalizado",
        widget=forms.TextInput(attrs={'placeholder': 'Escribe el nombre aquí', 'class': 'form-control'})
    )

    # Campos de "Estado"
    status_predefined = forms.ChoiceField(
        choices=STATUS_CHOICES,
        required=False,
        label="Estado Predefinido",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    status_custom = forms.CharField(
        required=False,
        label="Estado Personalizado",
        widget=forms.TextInput(attrs={
            'placeholder': 'Escribe un estado personalizado aquí',
            'class': 'form-control'
        })
    )

    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'priority']
        widgets = {
            'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        # Capturar la instancia actual para validar correctamente al actualizar
        self.instance = kwargs.get('instance')
        super().__init__(*args, **kwargs)

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if Task.objects.filter(title=title).exclude(id=self.instance.id).exists():
            raise forms.ValidationError("Ya existe una tarea con este título. Elige otro título.")
        return title

    def clean_assigned_to_predefined(self):
        predefined = self.cleaned_data.get('assigned_to_predefined')
        custom = self.cleaned_data.get('assigned_to_custom')

        if predefined == 'Otros' and not custom:
            raise forms.ValidationError('Si seleccionas "Otros", debes proporcionar un nombre personalizado.')
        if not predefined and not custom:
            raise forms.ValidationError('Debes seleccionar un usuario o proporcionar un nombre personalizado.')
        return predefined

    def clean_status_predefined(self):
        status_predefined = self.cleaned_data.get('status_predefined')
        status_custom = self.cleaned_data.get('status_custom')

        if status_predefined == 'Otros' and not status_custom:
            raise forms.ValidationError('Si seleccionas "Otros", debes proporcionar un estado personalizado.')
        if not status_predefined and not status_custom:
            raise forms.ValidationError('Debes seleccionar un estado predefinido o proporcionar uno personalizado.')
        return status_predefined

    def clean(self):
        cleaned_data = super().clean()

        # Asignar valores finales para "Asignado a"
        predefined = cleaned_data.get('assigned_to_predefined')
        custom = cleaned_data.get('assigned_to_custom')
        if predefined and predefined != 'Otros':
            cleaned_data['assigned_to'] = predefined
        elif custom:
            cleaned_data['assigned_to'] = custom

        # Asignar valores finales para "Estado"
        status_predefined = cleaned_data.get('status_predefined')
        status_custom = cleaned_data.get('status_custom')
        if status_predefined and status_predefined != 'Otros':
            cleaned_data['status_filter'] = status_predefined
        elif status_custom:
            cleaned_data['status_filter'] = status_custom

        return cleaned_data



# Nuevo formulario para la solución
class SolutionForm(forms.Form):
    solution = forms.CharField(
        label="Solución de la Tarea",
        widget=forms.Textarea(attrs={
            'placeholder': 'Describe la solución de la tarea aquí...',
            'rows': 4,
            'cols': 50,
            'class': 'form-control'
        }),
        required=True
    )
