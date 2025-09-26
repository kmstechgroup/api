from curses import meta
from dataclasses import field
from rest_framework.serializers import ModelSerializer, CharField
from rest_framework.viewsets import ViewSet
from ..models import User


class UserSerializer(ModelSerializer):
    class Meta:
        model=User
        fields = ["id", ]
        read_only_fields = ['id', 'email']  


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
    
