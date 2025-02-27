# Generated by Django 5.1.4 on 2025-01-22 13:36

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('description', models.TextField()),
                ('issue_link', models.URLField()),
                ('created_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Contributors',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('description', models.TextField()),
                ('priority', models.CharField(choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], max_length=16)),
                ('tag', models.CharField(choices=[('bug', 'Bug'), ('feature', 'Feature'), ('task', 'Task')], max_length=16)),
                ('status', models.CharField(choices=[('todo', 'Todo'), ('in_progress', 'In Progress'), ('finished', 'Finished')], max_length=16)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
                ('description', models.TextField()),
                ('type', models.CharField(choices=[('backend', 'Backend'), ('frontend', 'Frontend'), ('ios', 'Ios'), ('android', 'Android')], max_length=16)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
