from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    ASSIGN_TO_CHOICES = [
        ('Daniela Mazuera', 'Daniela Mazuera'),
        ('Sofia Puerto', 'Sofia Puerto'),
        ('Otros', 'Otros'),
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
