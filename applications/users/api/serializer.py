from rest_framework.serializers import ModelSerializer, CharField, PrimaryKeyRelatedField
from ..models import User, Allergy, ChronicDisease, PreviousSurgery, Disability



class AllergySerializer(ModelSerializer):
    class Meta:
        model = Allergy
        fields = ["id", "name"]

class ChronicDiseaseSerializer(ModelSerializer):
    class Meta:
        model = ChronicDisease
        fields = ["id", "name"]

class PreviousSurgerySerializer(ModelSerializer):
    class Meta:
        model = PreviousSurgery
        fields = ["id", "name"]

class DisabilitySerializer(ModelSerializer):
    class Meta:
        model = Disability
        fields = ["id", "name"]

class UserSerializer(ModelSerializer):
    allergies = AllergySerializer(many=True, read_only=True)
    allergies_ids = PrimaryKeyRelatedField(
        queryset=Allergy.objects.all(), many=True, write_only=True, source="allergies"
    )

    chronic_diseases = ChronicDiseaseSerializer(many=True, read_only=True)
    chronic_diseases_ids = PrimaryKeyRelatedField(
        queryset=ChronicDisease.objects.all(), many=True, write_only=True, source="chronic_diseases"
    )

    previous_surgeries = PreviousSurgerySerializer(many=True, read_only=True)
    previous_surgeries_ids = PrimaryKeyRelatedField(
        queryset=PreviousSurgery.objects.all(), many=True, write_only=True, source="previous_surgeries"
    )

    disabilities = DisabilitySerializer(many=True, read_only=True)
    disabilities_ids = PrimaryKeyRelatedField(
        queryset=Disability.objects.all(), many=True, write_only=True, source="disabilities"
    )

    class Meta:
        model = User
        fields = [
            "email","first_name", "last_name",
            "identificator", "address", "phone_number",
            "blood_type", "sex", "height", "weight", "age",
            
            # Relaciones
            "allergies", "allergies_ids", "allergies_other",
            "chronic_diseases", "chronic_diseases_ids", "chronic_diseases_other",
            "previous_surgeries", "previous_surgeries_ids", "previous_surgeries_other",
            "disabilities", "disabilities_ids", "disabilities_other",
            # Contactos de emergencia
            "close_contacts",
            # Estado
            "strikes", "blocked",
        ]
        read_only_fields = [
            "email",  "strikes", "blocked", 
        ]


class UserAdminSerializer(ModelSerializer):
    class Meta:
        model=User
        exclude = ['password',]
        
    
class UserRegisterSerializer(ModelSerializer):
    password = CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'identificator', 'password']
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            identificator=validated_data.get('identificator'),
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    

class GoogleLoginSerializer(ModelSerializer):
    # Solo lo recibimos en el request
    id_token = CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ["id", "email", "identificator", "id_token"]
        read_only_fields = ["id", "email"]