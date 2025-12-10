from drf_spectacular.utils import extend_schema
from rest_framework.viewsets import ModelViewSet
from ..models import Department
from .serializer import DepartmentSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .swagger_schemas import (
    department_list_schema,
    department_create_schema,
    department_retrieve_schema,
    department_update_schema,
    department_partial_update_schema,
    department_destroy_schema
)


class DepartmentViewSet(ModelViewSet):
    """
    ViewSet for CRUD operations on Department model.
    Provides full CRUD operations for emergency response departments.
    Only accessible by authenticated administrators.
    """
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAdminUser]
    
    @extend_schema(**department_list_schema())
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @extend_schema(**department_create_schema())
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @extend_schema(**department_retrieve_schema())
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @extend_schema(**department_update_schema())
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @extend_schema(**department_partial_update_schema())
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    @extend_schema(**department_destroy_schema())
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
