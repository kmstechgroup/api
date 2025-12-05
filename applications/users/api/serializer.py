from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, CharField, PrimaryKeyRelatedField
from ..models import User, Allergy, ChronicDisease, PreviousSurgery, Disability


# =============================================================================
# SERIALIZERS FOR RELATED MODELS
# =============================================================================

class AllergySerializer(ModelSerializer):
    """
    Serializer for the Allergy model.
    Serializes user allergies with their basic fields.
    """
    class Meta:
        model = Allergy
        fields = ["id", "name"]


class ChronicDiseaseSerializer(ModelSerializer):
    """
    Serializer for the ChronicDisease model.
    Serializes user chronic diseases.
    """
    class Meta:
        model = ChronicDisease
        fields = ["id", "name"]


class PreviousSurgerySerializer(ModelSerializer):
    """
    Serializer for the PreviousSurgery model.
    Serializes user previous surgeries.
    """
    class Meta:
        model = PreviousSurgery
        fields = ["id", "name"]


class DisabilitySerializer(ModelSerializer):
    """
    Serializer for the Disability model.
    Serializes user disabilities.
    """
    class Meta:
        model = Disability
        fields = ["id", "name"]

# =============================================================================
# MAIN USER SERIALIZER
# =============================================================================

class UserSerializer(ModelSerializer):
    """
    Main serializer for the User model.
    
    Features:
    - Handles many-to-many relationships with separate fields for read/write
    - Includes personal, medical, and contact information fields
    - Allows authenticated user profile updates
    """
    
    # Read-only fields to display complete objects
    allergies = AllergySerializer(many=True, read_only=True)
    chronic_diseases = ChronicDiseaseSerializer(many=True, read_only=True)
    previous_surgeries = PreviousSurgerySerializer(many=True, read_only=True)
    disabilities = DisabilitySerializer(many=True, read_only=True)
    
    # Write-only fields to receive IDs and update relationships
    allergies_ids = PrimaryKeyRelatedField(
        queryset=Allergy.objects.all(), 
        many=True, 
        write_only=True, 
        source="allergies"
    )
    chronic_diseases_ids = PrimaryKeyRelatedField(
        queryset=ChronicDisease.objects.all(), 
        many=True, 
        write_only=True, 
        source="chronic_diseases"
    )
    previous_surgeries_ids = PrimaryKeyRelatedField(
        queryset=PreviousSurgery.objects.all(), 
        many=True, 
        write_only=True, 
        source="previous_surgeries"
    )
    disabilities_ids = PrimaryKeyRelatedField(
        queryset=Disability.objects.all(), 
        many=True, 
        write_only=True, 
        source="disabilities"
    )

    class Meta:
        model = User
        fields = [
            # Basic personal information
            "email", "first_name", "last_name", "identificator", 
            "address", "phone_number",
            
            # Medical information
            "blood_type", "sex", "height", "weight", "birthdate",
            
            # Medical relationships (with free text fields for "others")
            "allergies", "allergies_ids", "allergies_other",
            "chronic_diseases", "chronic_diseases_ids", "chronic_diseases_other",
            "previous_surgeries", "previous_surgeries_ids", "previous_surgeries_other",
            "disabilities", "disabilities_ids", "disabilities_other",
            
            # Emergency contacts
            "close_contacts",
            
            # User status (read-only)
            "strikes", "blocked",
        ]
        read_only_fields = [
            "email",    # Email cannot be changed once created
            "strikes",  # Strikes are managed by the system
            "blocked",  # Blocking is managed by administrators
        ]


# =============================================================================
# ADMIN AND AUTHENTICATION SERIALIZERS
# =============================================================================

class UserAdminSerializer(ModelSerializer):
    """
    Serializer for admin operations on User model.
    Excludes password field for security reasons.
    Used by administrators to manage user data.
    """
    class Meta:
        model = User
        exclude = ['password',]  # Exclude password for security
        

class UserRegisterSerializer(ModelSerializer):
    """
    Serializer for user registration.
    Handles user creation with password hashing.
    """
    password = CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'identificator', 'password']
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        """
        Create a new user with hashed password.
        """
        user = User(
            email=validated_data['email'],
            identificator=validated_data.get('identificator'),
        )
        user.set_password(validated_data['password'])  # Hash the password
        user.save()
        return user
    

class GoogleLoginSerializer(ModelSerializer):
    """
    Serializer for Google OAuth login.
    Receives Google ID token and validates it.
    """
    # Only received in the request, not stored
    id_token = CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ["id", "email", "identificator", "id_token"]
        read_only_fields = ["id", "email"]


# =============================================================================
# MEDICAL OPTIONS RESPONSE SERIALIZER
# =============================================================================

class MedicalOptionsResponseSerializer(serializers.Serializer):
    """
    Serializer for medical options response.
    Contains all active medical options grouped by type.
    """
    allergies = AllergySerializer(many=True, read_only=True)
    chronic_diseases = ChronicDiseaseSerializer(many=True, read_only=True)
    previous_surgeries = PreviousSurgerySerializer(many=True, read_only=True)
    disabilities = DisabilitySerializer(many=True, read_only=True)


# =============================================================================
# ADMIN SERIALIZERS FOR MEDICAL OPTIONS (CRUD)
# =============================================================================

class AllergyAdminSerializer(ModelSerializer):
    """
    Admin serializer for Allergy model.
    Includes all fields for CRUD operations.
    """
    class Meta:
        model = Allergy
        fields = ["id", "name", "is_active", "created_at"]
        read_only_fields = ["created_at"]


class ChronicDiseaseAdminSerializer(ModelSerializer):
    """
    Admin serializer for ChronicDisease model.
    Includes all fields for CRUD operations.
    """
    class Meta:
        model = ChronicDisease
        fields = ["id", "name", "is_active", "created_at"]
        read_only_fields = ["created_at"]


class PreviousSurgeryAdminSerializer(ModelSerializer):
    """
    Admin serializer for PreviousSurgery model.
    Includes all fields for CRUD operations.
    """
    class Meta:
        model = PreviousSurgery
        fields = ["id", "name", "is_active", "created_at"]
        read_only_fields = ["created_at"]


class DisabilityAdminSerializer(ModelSerializer):
    """
    Admin serializer for Disability model.
    Includes all fields for CRUD operations.
    """
    class Meta:
        model = Disability
        fields = ["id", "name", "is_active", "created_at"]
        read_only_fields = ["created_at"]