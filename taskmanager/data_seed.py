from django.contrib.auth.models import User

users_data = [
    {'username': 'danielamazuera', 'password': 'KENNEDY2024.', 'first_name': 'Daniela', 'last_name': 'Mazuera'},
    {'username': 'sofiapuerto', 'password': 'KENNEDY2024.', 'first_name': 'Sofia', 'last_name': 'Puerto'},
    {'username': 'danielcampos', 'password': 'KENNEDY2024.', 'first_name': 'Daniel', 'last_name': 'Campos'},
]

for user_data in users_data:
    user, created = User.objects.get_or_create(username=user_data['username'])
    if created:
        user.set_password(user_data['password'])
        user.first_name = user_data['first_name']
        user.last_name = user_data['last_name']
        user.save()
