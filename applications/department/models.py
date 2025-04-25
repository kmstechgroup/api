from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

app_name='department'

#Model Department
class Department(models.Model):
    TYPE_DEPARTMENT = [
        ('Bomberos', 'firefighters'),
        ('Policia','police')
    ]

    code_department = models.AutoField(primary_key=True, unique=True)
    type_department = models.CharField(choices=TYPE_DEPARTMENT)
    name_department = models.CharField(max_length=50)
    jurisdiction = models.JSONField()
    city_center_lat = models.FloatField()
    city_center_lon = models.FloatField()
    phone = models.BigIntegerField() 

    def __str__(self):
        return f"Departmento #{self.code_department}"

class CommunicateEmergencyDepartment(models.Model):
    code_department = models.ForeignKey(
        'department.Department',
        on_delete=models.CASCADE,
        related_name='emergency_communications'
    ),
    code_emergency = models.ForeignKey(
        'alarm.Emergency',
        on_delete=models.CASCADE,
        related_name='department_communications'
    ),
    is_close = models.BooleanField(default=False)
    def __str__(self):
        return f"Emergencia {self.code_emergency} - Departmento {self.code_department} - Close: {self.is_close}"

