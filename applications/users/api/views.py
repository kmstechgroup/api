from django.views.generic import View
from drf_spectacular.utils import extend_schema, OpenApiParameter,inline_serializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from ..models import User
from .serializer import UserRegisterSerializer, UserAdminSerializer, UserSerializer
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework import serializers
from .services import login_user



class UserViewSet(ViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=["get", "patch"])
    def profile(self, request):
        if request.method == "GET":
            serializer = UserSerializer(request.user)
            return Response(serializer.data)
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UsersAdminViewSet(ModelViewSet):
    
    queryset = User.objects.all()
    serializer_class = UserAdminSerializer
    permission_classes = [IsAdminUser]
    
class UserRegisterView(ViewSet):
    permission_classes = [AllowAny]
    
    @extend_schema(
        request=UserRegisterSerializer,   # qué espera en el body
        responses=UserRegisterSerializer  # qué devuelve si todo va bien
    )
    
    #@action(detail=False, methods=['post'])
    def create(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserLoginView(ViewSet):
    
    @extend_schema(
        request=inline_serializer(
            name="LoginRequest",
            fields={
                "email": serializers.EmailField(),
                "identificator": serializers.IntegerField(),
                "password": serializers.CharField(),
            }
        ),
        responses=inline_serializer(
            name="LoginResponse",
            fields={
                "token": serializers.CharField(),
                "error": serializers.CharField(required=False),
            }
        ),
    )
    
    def create(self, request):
        user = login_user(email=request.data['email'], password=request.data['password'], identificator=request.data['identificator'])
        print(f"User:{user}")
        if 'error' in user:
            return Response(user, status=status.HTTP_401_UNAUTHORIZED)
        
        return Response(user, status=status.HTTP_202_ACCEPTED)
    
    
