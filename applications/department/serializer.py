from rest_framework import serializers
from .models import Department

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Department
        fields =(
            'code_department',
            'type_department',
            'name_department',
            'jurisdiction',
            'city_center_lat',
            'city_center_lon',
            'phone',
        )
