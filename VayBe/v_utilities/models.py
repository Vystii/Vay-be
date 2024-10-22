from django.db import models

# Create your models here.

class ModelBase(models.Model):
    STUDIES_LEVELS = [
        ('L1', 'Licence 1'),
        ('L2', 'Licence 2'),
        ('L3', 'Licence 3'),
        ('M1', 'Master 1'),
        ('M2', 'Master 2')
    ]

    studies_level = models.CharField(
        max_length=2,
        choices=STUDIES_LEVELS,
        default='L1',
    )
    
    class Meta:
        abstract = True