from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from applications.department.models import Department
from applications.users.models import User

app_name='alarm'

#Model Emergency
class Emergency(models.Model):
    code_emergency = models.AutoField(primary_key=True)
    date_time = models.DateTimeField(auto_now_add=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    created_by = models.ForeignKey(
        'users.User',
        default=10000001,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name='related_users'
    )
    emergency_main = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='related_emergencies'
    )
    department = models.ManyToManyField(
        Department,
        through = 'CommunicateEmergencyDepartment',
        related_name= 'Emergency_Department'
    )

    def __str__(self):
        return f"Emergency {self.code_emergency} Department: {self.department}"
    
#Model Department-Emergency

class CommunicateEmergencyDepartment(models.Model):
    code_department = models.ForeignKey(
        'department.Department',
        on_delete=models.CASCADE,
        related_name='emergency_communications'
    )
    code_emergency = models.ForeignKey(
        'alarm.Emergency',
        on_delete=models.CASCADE,
        related_name='department_communications'
    )
    is_close = models.BooleanField(default=False)
    def __str__(self):
        return f"Emergencia {self.code_emergency} - Departmento {self.code_department} - Close: {self.is_close}"
