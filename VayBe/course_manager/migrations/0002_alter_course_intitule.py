# Generated by Django 5.1.2 on 2024-10-22 01:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course_manager', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='intitule',
            field=models.CharField(default=None, max_length=7, verbose_name='course label'),
        ),
    ]