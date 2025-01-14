# Generated by Django 5.1.2 on 2025-01-04 22:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('v_utilities', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='study_field',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='v_utilities.studyfield', verbose_name='study field'),
        ),
        migrations.AlterField(
            model_name='users',
            name='study_level',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='v_utilities.studylevel', verbose_name='studies level'),
        ),
    ]
