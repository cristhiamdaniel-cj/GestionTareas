from django.contrib.auth.models import User
from decouple import config  # Importa la función config de python-decouple

# Datos de usuarios
users_data = [
    {'username': 'danielamazuera', 'password': config('USER1_PASS'), 'first_name': 'Daniela', 'last_name': 'Mazuera'},
    {'username': 'sofiapuerto', 'password': config('USER2_PASS'), 'first_name': 'Sofia', 'last_name': 'Puerto'},
    {'username': 'danielcampos', 'password': config('SUPERUSER_PASS'), 'first_name': 'Daniel', 'last_name': 'Campos'},
]

# Crear usuarios
for user_data in users_data:
    user, created = User.objects.get_or_create(username=user_data['username'])
    if created:
        user.set_password(user_data['password'])
        user.first_name = user_data['first_name']
        user.last_name = user_data['last_name']
        if user_data['username'] == 'danielcampos':  # Hace que danielcampos sea superusuario
            user.is_superuser = True
            user.is_staff = True
        user.save()
        print(f"Usuario {user_data['username']} creado correctamente.")
    else:
        print(f"El usuario {user_data['username']} ya existe.")
