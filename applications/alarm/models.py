from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


#Model Client
class Client(models.Model):
    code_client = models.AutoField(primary_key=True, unique=True)
    jurisdiction = models.JSONField()
    city_center_lat = models.FloatField()
    city_center_lon = models.FloatField()
    phone = models.BigIntegerField() 

    def __str__(self):
        return f"Client #{self.code_client}"

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
    
#Model Client-Emergency
class CommunicateEmergencyClient(models.Model):
    code_client = models.ForeignKey(
        'Client',
        on_delete=models.CASCADE,
        related_name='emergency_communications'
    )
    code_emergency = models.ForeignKey(
        'Emergency',
        on_delete=models.CASCADE,
        related_name='client_communications'
    )
    is_close = models.BooleanField(default=False)
    def __str__(self):
        return f"Emergency {self.code_emergency_id} - Client {self.code_client_id} - Close: {self.is_close}"

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
        ('F', 'Female')
        ('X', 'Prefere not to say')
    ]

    id = models.IntegerField(
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
    emergency_code = models.ForeignKey(Emergency, on_delete=models.Cascade, null=True)

    def __str__(self):
        return f"{self.name} {self.last_name}"
