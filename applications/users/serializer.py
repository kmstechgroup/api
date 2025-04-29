from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields =(
            'dni',
            'name',
            'last_name',
            'address',
            'blood_type',
            'sex',
            'height_cm',
            'weight_kg',
            'age',
            'allergies',
            'chronic_diseases',
            'previous_surgeries',
            'disabilities',
            'close_contacts',
        )