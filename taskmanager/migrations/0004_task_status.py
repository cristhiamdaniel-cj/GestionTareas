# Generated by Django 5.1.4 on 2024-12-11 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taskmanager', '0003_auditlog_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('completed', 'Completado'), ('in_progress', 'En Proceso')], default='in_progress', max_length=20),
        ),
    ]
