# Generated by Django 5.1.2 on 2024-10-22 04:27

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='users',
            options={'permissions': [('handle_request', 'Can handle request')]},
        ),
        migrations.AlterField(
            model_name='users',
            name='studies_level',
            field=models.CharField(choices=[('L1', 'Licence 1'), ('L2', 'Licence 2'), ('L3', 'Licence 3'), ('M1', 'Master 1'), ('M2', 'Master 2')], default='L1', max_length=2),
        ),
        migrations.CreateModel(
            name='SchoolRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('receiver', models.ForeignKey(limit_choices_to={'is_request_handler': True}, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='receiver')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='sender')),
            ],
        ),
    ]