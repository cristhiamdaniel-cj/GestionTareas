from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    ASSIGN_TO_CHOICES = [
        ('Daniela Mazuera', 'Daniela Mazuera'),
        ('Sofia Puerto', 'Sofia Puerto'),
        ('Otros', 'Otros'),
        ('Sin asignar', 'Sin asignar'),
    ]

    assigned_to_predefined = forms.ChoiceField(
        choices=ASSIGN_TO_CHOICES,
        required=False,
        label="Asignado a"
    )
    assigned_to_custom = forms.CharField(
        required=False,
        label="Nombre Personalizado",
        widget=forms.TextInput(attrs={'placeholder': 'Escribe el nombre aquí'})
    )

    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'priority']
        widgets = {
            'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'priority': forms.Select(),
        }

    # Validación para el campo 'title'
    def clean_title(self):
        title = self.cleaned_data.get('title')
        instance = self.instance  # Obtener la instancia actual (si existe)

        # Verificar si ya existe un título duplicado (ignorar la misma instancia en actualizaciones)
        if Task.objects.filter(title=title).exclude(pk=instance.pk).exists():
            raise forms.ValidationError("Ya existe una tarea con este título. Elige otro título.")
        return title

    # Validación de asignado a
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
            cleaned_data['assigned_to'] = "Sin asignar"  # Valor por defecto si no se selecciona nada

        return cleaned_data
