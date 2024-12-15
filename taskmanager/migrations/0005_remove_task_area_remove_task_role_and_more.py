# Generated by Django 5.1.4 on 2024-12-15 23:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taskmanager', '0004_task_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='area',
        ),
        migrations.RemoveField(
            model_name='task',
            name='role',
        ),
        migrations.RemoveField(
            model_name='task',
            name='subgroup',
        ),
        migrations.AddField(
            model_name='task',
            name='solution',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='title',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
