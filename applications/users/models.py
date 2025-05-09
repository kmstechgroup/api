from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
app_name='users'

#Model User
class UserCustom(AbstractUser):
    BLOOD_TYPES = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-'),
    ]

    SEX_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('X', 'Prefere not to say'),
    ]

    dni = models.IntegerField(
        validators=[
            MinValueValidator(10000000),
            MaxValueValidator(99999999)
        ], null=True, blank=True
    )
    address = models.CharField(max_length=100, default='')
    blood_type = models.CharField(max_length=3, choices=BLOOD_TYPES, default='')
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, default='')
    height_cm = models.PositiveIntegerField(null=True, blank=True)
    weight_kg = models.PositiveIntegerField(null=True, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    
    allergies = models.TextField(blank=True)
    chronic_diseases = models.TextField(blank=True)
    previous_surgeries = models.TextField(blank=True)
    disabilities = models.TextField(blank=True)
    close_contacts = models.JSONField(default=dict, blank=True)
    
    #---Attributes of Django's User model---
    groups = models.ManyToManyField(
        Group,
        related_name='usercustom_set',
        blank=True,
        help_text="The groups this user belongs to."
    )
    
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='usercustom_permissions',
        blank=True,
        help_text="Specific permissions for this user."
    )
    

    def __str__(self):
        return f"{self.name} {self.last_name}"
