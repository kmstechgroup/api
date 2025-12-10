import uuid
from django.db import models
from applications.users.models import User


class Emergency(models.Model):
    """Emergency model representing emergency incidents."""
    
    EMERGENCY_STATUS_CHOICES = [
        ('open', 'Open'),
        ('standby', 'Standby'),
        ('in_progress', 'In Progress'),
        ('close', 'Close'),
    ]
    
    TYPE_EMERGENCY_CHOICES = [
        ('vehicular_accident', 'Accident'),
        ('sanitary_assistance', 'Sanitary Assistance'),
        ('Fire', 'Fire'),
    ]
    
    code_emergency = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    date_time = models.DateTimeField()
    lat = models.DecimalField(max_digits=10, decimal_places=8, blank=True, null=True)
    lon = models.DecimalField(max_digits=11, decimal_places=8, blank=True, null=True)
    emergency_status = models.CharField(
        max_length=20,
        choices=EMERGENCY_STATUS_CHOICES,
        default='open'
    )
    type_emergency = models.CharField(
        max_length=20,
        choices=TYPE_EMERGENCY_CHOICES,
        default='sanitary_assistance'
    )
    subtype_emergency = models.CharField(max_length=100, blank=True, null=True)
    date_open = models.DateTimeField(blank=True, null=True)
    date_standby = models.DateTimeField(blank=True, null=True)
    date_in_progress = models.DateTimeField(blank=True, null=True)
    date_close = models.DateTimeField(blank=True, null=True)
    
    # Foreign Keys
    emergency_main = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='sub_emergencies',
        help_text="Main emergency if this is a sub-emergency"
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='created_emergencies',
        help_text="User who created the emergency"
    )
    
    # Many-to-many relationship with Department through ComunicateEmergencyDepartment
    departments = models.ManyToManyField(
        'department.Department',
        through='ComunicateEmergencyDepartment',
        related_name='emergencies'
    )
    
    class Meta:
        db_table = 'emergency'
        verbose_name = 'Emergency'
        verbose_name_plural = 'Emergencies'
        ordering = ['-date_time']
    
    def __str__(self):
        return f"Emergency {self.code_emergency} - {self.type_emergency or 'Unknown'}"


class ComunicateEmergencyDepartment(models.Model):
    """Junction table for many-to-many relationship between Emergency and Department."""
    
    code_emergency = models.ForeignKey(
        'Emergency',
        on_delete=models.CASCADE,
        related_name='department_communications'
    )
    code_department = models.ForeignKey(
        'department.Department',
        on_delete=models.CASCADE,
        related_name='emergency_communications'
    )
    
    class Meta:
        db_table = 'comunicate_emergency_department'
        verbose_name = 'Emergency Department Communication'
        verbose_name_plural = 'Emergency Department Communications'
        unique_together = [['code_emergency', 'code_department']]
    
    def __str__(self):
        return f"{self.code_emergency} - {self.code_department}"
