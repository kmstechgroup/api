import uuid
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser

app_name = 'users'


class Allergy(models.Model):
    """Predefined allergy options."""
    name = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Allergy'
        verbose_name_plural = 'Allergies'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class ChronicDisease(models.Model):
    """Predefined chronic disease options."""
    name = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Chronic Disease'
        verbose_name_plural = 'Chronic Diseases'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class PreviousSurgery(models.Model):
    """Predefined previous surgery options."""
    name = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Previous Surgery'
        verbose_name_plural = 'Previous Surgeries'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Disability(models.Model):
    """Predefined disability options."""
    name = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Disability'
        verbose_name_plural = 'Disabilities'
        ordering = ['name']
    
    def __str__(self):
        return self.name

class User(AbstractUser):
    """
    Custom user model for app users only.
    Simple model without Django auth complexity.
    Based on the UML class diagram.
    """
    
    BLOOD_TYPES = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-'),
    ]

    SEX_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('X', 'Prefer not to say'),
    ]
    
    
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    email = models.EmailField(unique=True)
    username = models.CharField(
        max_length=30,
        unique=True,
        blank=True,
        null=True,
    )
       
    # Additional fields for OAuth with Google
    google_id = models.CharField(
        max_length=255, 
        blank=True, 
        null=True, 
        unique=True,
        help_text="Unique Google ID for OAuth users"
    )
    is_oauth_user = models.BooleanField(
        default=False,
        help_text="Indicates if user registered with OAuth"
    )
    
    identificator = models.BigIntegerField(
        blank=True,
        null=True,
        help_text="DNI, passport or other identity document number"
    )
    address = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="User's address"
    )
    
    # Medical information
    blood_type = models.CharField(
        max_length=3, 
        choices=BLOOD_TYPES, 
        blank=True, 
        null=True
    )
    sex = models.CharField(
        max_length=1, 
        choices=SEX_CHOICES, 
        blank=True, 
        null=True
    )
    height = models.PositiveIntegerField(
        blank=True, 
        null=True,
        help_text="Height in centimeters"
    )
    weight = models.PositiveIntegerField(
        blank=True, 
        null=True,
        help_text="Weight in kilograms"
    )
    birthdate = models.DateField(
        blank=True, 
        null=True,
        help_text="User's date of birth"
    )
    
    # Detailed medical information - ManyToMany relationships for predefined options
    allergies = models.ManyToManyField(
        Allergy,
        blank=True,
        related_name='users_with_allergy',
        help_text="Predefined allergy options"
    )
    chronic_diseases = models.ManyToManyField(
        ChronicDisease,
        blank=True,
        related_name='users_with_disease',
        help_text="Predefined chronic disease options"
    )
    previous_surgeries = models.ManyToManyField(
        PreviousSurgery,
        blank=True,
        related_name='users_with_surgery',
        help_text="Predefined previous surgery options"
    )
    disabilities = models.ManyToManyField(
        Disability,
        blank=True,
        related_name='users_with_disability',
        help_text="Predefined disability options"
    )
    
    # Custom text fields for "Other" options
    allergies_other = models.TextField(
        blank=True,
        null=True,
        help_text="Other allergies not in predefined list"
    )
    chronic_diseases_other = models.TextField(
        blank=True,
        null=True,
        help_text="Other chronic diseases not in predefined list"
    )
    previous_surgeries_other = models.TextField(
        blank=True,
        null=True,
        help_text="Other previous surgeries not in predefined list"
    )
    disabilities_other = models.TextField(
        blank=True,
        null=True,
        help_text="Other disabilities not in predefined list"
    )
    
    # Emergency contacts
    close_contacts = models.JSONField(
        default=dict,
        help_text="Emergency contacts in JSON format"
    )
    
    # Contact information
    phone_number = models.PositiveBigIntegerField(
        blank=True, 
        null=True,
        help_text="Phone number as positive integer"
    )
    
    # Warning system
    strikes = models.PositiveIntegerField(
        default=0,
        help_text="Number of warnings or infractions"
    )
    
    # Blocked status
    blocked = models.BooleanField(
        default=False,
        help_text="Indicates if user is blocked"
    )
    
    # Audit fields
    updated_at = models.DateTimeField(auto_now=True)
    
    # Model configuration
    USERNAME_FIELD = "email"  
    REQUIRED_FIELDS = ["username"]
    
    class Meta:
        db_table = 'user'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"
    
    @property
    def full_name(self):
        """Returns the user's full name."""
        return f"{self.first_name} {self.last_name}".strip()
    
    def is_google_user(self):
        """Checks if user registered with Google OAuth."""
        return bool(self.google_id)
    
    
    # Medical information helper methods
    def get_all_allergies(self):
        """Returns all allergies (predefined + custom)."""
        predefined = list(self.allergies.values_list('name', flat=True))
        custom = self.allergies_other.split('\n') if self.allergies_other else []
        return predefined + [item.strip() for item in custom if item.strip()]
    
    def get_all_chronic_diseases(self):
        """Returns all chronic diseases (predefined + custom)."""
        predefined = list(self.chronic_diseases.values_list('name', flat=True))
        custom = self.chronic_diseases_other.split('\n') if self.chronic_diseases_other else []
        return predefined + [item.strip() for item in custom if item.strip()]
    
    def get_all_previous_surgeries(self):
        """Returns all previous surgeries (predefined + custom)."""
        predefined = list(self.previous_surgeries.values_list('name', flat=True))
        custom = self.previous_surgeries_other.split('\n') if self.previous_surgeries_other else []
        return predefined + [item.strip() for item in custom if item.strip()]
    
    def get_all_disabilities(self):
        """Returns all disabilities (predefined + custom)."""
        predefined = list(self.disabilities.values_list('name', flat=True))
        custom = self.disabilities_other.split('\n') if self.disabilities_other else []
        return predefined + [item.strip() for item in custom if item.strip()]

