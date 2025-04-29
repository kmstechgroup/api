from rest_framework import serializers
from .models import Emergency, CommunicateEmergencyDepartment

app_name='alarm'

class EmergencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Emergency
        fields = (
            'code_emergency',
            'date_time',
            'latitude',
            'longitude',
            'emergency_main'   
            )   


class CommunicateEmergencyDepartmentSerializer(serializers.ModelSerializer):
    class Meta: 
        model = CommunicateEmergencyDepartment
        fields = '__all__'
        depth = 1