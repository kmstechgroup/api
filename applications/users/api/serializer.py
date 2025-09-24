from rest_framework.serializers import ModelSerializer, CharField
from ..models import User

class UserRegisterSerializer(ModelSerializer):
    password = CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id_user', 'email', 'identificator', 'password', 'date_joined']

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            identificator=validated_data.get('identificator'),
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
