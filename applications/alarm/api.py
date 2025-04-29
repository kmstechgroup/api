from .models import Emergency, CommunicateEmergencyDepartment
from rest_framework import viewsets, permissions
from .serializer import EmergencySerializer, CommunicateEmergencyDepartmentSerializer

class EmergencyViewSet(viewsets.ModelViewSet):
    queryset = Emergency.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = EmergencySerializer


class CommunicateEmergencyDepartmentViewSet(viewsets.ModelViewSet):
    queryset = CommunicateEmergencyDepartment.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = CommunicateEmergencyDepartmentSerializer