# Generated by Django 5.1.2 on 2025-01-04 06:13

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SiteConfiguration',
            fields=[
                ('config_name', models.CharField(max_length=255, primary_key=True, serialize=False, verbose_name='Config name')),
                ('config_value', models.TextField(blank=True, null=True, verbose_name='Value')),
            ],
            options={
                'verbose_name': 'Site Configuration',
                'verbose_name_plural': 'Site Configurations',
            },
        ),
        migrations.CreateModel(
            name='StudyField',
            fields=[
                ('code', models.CharField(max_length=5, primary_key=True, serialize=False, validators=[django.core.validators.RegexValidator('^[A-Z]{3}')], verbose_name='code')),
                ('label', models.CharField(max_length=20, verbose_name='label')),
            ],
        ),
        migrations.CreateModel(
            name='StudyLevel',
            fields=[
                ('level', models.IntegerField(unique=True, validators=[django.core.validators.MinValueValidator(1)], verbose_name='level')),
                ('code', models.CharField(max_length=5, primary_key=True, serialize=False, verbose_name='code level')),
                ('label', models.CharField(max_length=20, verbose_name='label')),
            ],
        ),
    ]