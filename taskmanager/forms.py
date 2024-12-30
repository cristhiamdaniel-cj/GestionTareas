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

    # Validación para título único (ignorar al actualizar)
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if Task.objects.filter(title=title).exclude(id=self.instance.id).exists():
            raise forms.ValidationError("Ya existe una tarea con este título. Elige otro título.")
        return title

    # Validación de los campos "Asignado a"
    def clean(self):
        cleaned_data = super().clean()
        predefined = cleaned_data.get('assigned_to_predefined')
        custom = cleaned_data.get('assigned_to_custom')

        if predefined == 'Otros' and not custom:
            self.add_error('assigned_to_custom', 'Debes proporcionar un nombre si seleccionas "Otros".')
        elif predefined and predefined != 'Otros':
            cleaned_data['assigned_to'] = predefined
        elif custom:
            cleaned_data['assigned_to'] = custom
        else:
            self.add_error('assigned_to_predefined', 'Debes seleccionar o proporcionar un nombre.')

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
