from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
app_name='users'

#Model User
class User(models.Model):
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
        primary_key=True,
        validators=[
            MinValueValidator(10000000),
            MaxValueValidator(99999999)
        ]
    )
    name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    address = models.CharField(max_length=100)

    blood_type = models.CharField(max_length=3, choices=BLOOD_TYPES)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES)

    height_cm = models.PositiveIntegerField()
    weight_kg = models.PositiveIntegerField()
    age = models.PositiveIntegerField()

    allergies = models.TextField(blank=True)
    chronic_diseases = models.TextField(blank=True)
    previous_surgeries = models.TextField(blank=True)
    disabilities = models.TextField(blank=True)

    close_contacts = models.JSONField(default=dict)

    def __str__(self):
        return f"{self.name} {self.last_name}"
