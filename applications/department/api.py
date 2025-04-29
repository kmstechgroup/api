from .models import Department 
from rest_framework import viewsets, permissions
from .serializer import DepartmentSerializer 

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = DepartmentSerializer

