# =============================================================================
# SWAGGER SCHEMAS FOR API DOCUMENTATION
# =============================================================================

from drf_spectacular.utils import inline_serializer
from rest_framework import serializers
from .serializer import DepartmentSerializer


# =============================================================================
# DEPARTMENT CRUD SCHEMAS
# =============================================================================

def department_list_schema():
    return {
        "summary": "List all departments",
        "description": "Retrieve a list of all emergency response departments. Only accessible by authenticated administrators.",
        "tags": ["Departments"]
    }

def department_create_schema():
    return {
        "summary": "Create a new department",
        "description": "Create a new emergency response department. The jurisdiction_expanded field is automatically calculated as a 1km buffer around the jurisdiction. Only accessible by authenticated administrators.",
        "request": DepartmentSerializer,
        "responses": {
            201: DepartmentSerializer,
            400: inline_serializer(
                name="DepartmentCreateError",
                fields={
                    "field_name": serializers.ListField(child=serializers.CharField()),
                }
            )
        },
        "tags": ["Departments"]
    }

def department_retrieve_schema():
    return {
        "summary": "Get department details",
        "description": "Retrieve detailed information about a specific emergency response department including its jurisdiction and expanded jurisdiction. Only accessible by authenticated administrators.",
        "responses": {
            200: DepartmentSerializer,
            404: inline_serializer(
                name="DepartmentNotFound",
                fields={
                    "detail": serializers.CharField(help_text="Department not found"),
                }
            )
        },
        "tags": ["Departments"]
    }

def department_update_schema():
    return {
        "summary": "Update department (full)",
        "description": "Update all fields of a department. The jurisdiction_expanded field will be automatically recalculated if jurisdiction is updated. Only accessible by authenticated administrators.",
        "request": DepartmentSerializer,
        "responses": {
            200: DepartmentSerializer,
            400: inline_serializer(
                name="DepartmentUpdateError",
                fields={
                    "field_name": serializers.ListField(child=serializers.CharField()),
                }
            )
        },
        "tags": ["Departments"]
    }

def department_partial_update_schema():
    return {
        "summary": "Update department (partial)",
        "description": "Partially update department fields. The jurisdiction_expanded field will be automatically recalculated if jurisdiction is updated. Only accessible by authenticated administrators.",
        "request": DepartmentSerializer,
        "responses": {
            200: DepartmentSerializer,
            400: inline_serializer(
                name="DepartmentPartialUpdateError",
                fields={
                    "field_name": serializers.ListField(child=serializers.CharField()),
                }
            )
        },
        "tags": ["Departments"]
    }

def department_destroy_schema():
    return {
        "summary": "Delete department",
        "description": "Delete an emergency response department. Only accessible by authenticated administrators.",
        "responses": {
            204: None,
            404: inline_serializer(
                name="DepartmentNotFound",
                fields={
                    "detail": serializers.CharField(help_text="Department not found"),
                }
            )
        },
        "tags": ["Departments"]
    }
