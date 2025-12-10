import uuid
from django.contrib.gis.db import models


class Department(models.Model):
    """Department model representing emergency response departments."""
    
    code_department = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, blank=True, null=True)
    phone = models.PositiveBigIntegerField(
        blank=True, 
        null=True,
        help_text="Phone number as positive integer"
    )
    email = models.EmailField(blank=True, null=True)
    jurisdiction = models.PolygonField(
        blank=True,
        null=True,
        help_text="GeoJSON polygon representing the department's jurisdiction"
    )
    jurisdiction_expanded = models.PolygonField(
        blank=True,
        null=True,
        help_text="Auto-calculated: jurisdiction expanded by 1km buffer"
    )
    
    class Meta:
        db_table = 'department'
        verbose_name = 'Department'
        verbose_name_plural = 'Departments'
        ordering = ['name']
    
    def __str__(self):
        return self.name
