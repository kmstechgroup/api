from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from applications.department.models import *

app_name='alarm'
#Model Emergency
class Emergency(models.Model):
    code_emergency = models.AutoField(primary_key=True)
    date_time = models.DateTimeField(auto_now_add=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    emergency_main = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='related_emergencies'
    )

    def __str__(self):
        return f"Emergency {self.code_emergency}"
    
#Model Department-Emergency
