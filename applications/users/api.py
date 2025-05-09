from .models import UserCustom
from rest_framework import viewsets, permissions
from .serializer import UserSerializer
from rest_framework.permissions import BasePermission, IsAuthenticated

class UserViewSet(viewsets.ModelViewSet):
    queryset = UserCustom.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer