from .models import UserCustom
from rest_framework import viewsets, permissions
from .serializer import UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = UserCustom.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer