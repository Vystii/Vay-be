from django.db import models

# Create your models here.

class ModelBase(models.Model):
    STUDIES_LEVELS = [
        ('L1', 'Active'),
        ('L2', 'Inactive'),
        ('L3', 'Pending'),
        ('M1', 'Pending'),
        ('M2', 'Pending')
    ]

    studies_level = models.CharField(
        max_length=2,
        choices=STUDIES_LEVELS,
        default='L1',
    )
    
    class Meta:
        abstract = True