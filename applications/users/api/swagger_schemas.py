# =============================================================================
# SWAGGER SCHEMAS FOR API DOCUMENTATION
# =============================================================================

from drf_spectacular.utils import inline_serializer
from rest_framework import serializers
from .serializer import (
    UserSerializer, UserRegisterSerializer, GoogleLoginSerializer,
    MedicalOptionsResponseSerializer
)


# =============================================================================
# USER PROFILE SCHEMAS
# =============================================================================

def user_profile_schema():
    """Schema for user profile GET/PATCH endpoint"""
    return {
        "summary": "Get or update user profile",
        "description": "GET: Retrieve the authenticated user's profile information including personal data, medical information, and emergency contacts. PATCH: Update the authenticated user's profile information. Only provided fields will be updated (partial update).",
        "request": UserSerializer,
        "responses": {
            200: UserSerializer,
            400: inline_serializer(
                name="ProfileUpdateError",
                fields={
                    "field_name": serializers.ListField(child=serializers.CharField()),
                }
            )
        },
        "tags": ["User Profile"]
    }

def user_reset_profile_schema():
    """Schema for user profile reset endpoint"""
    return {
        "summary": "Reset user profile data",
        "description": "Reset all user profile data to null, keeping only essential fields: id, password, email, identificator, is_active, last_login, date_joined, is_oauth_user, is_superuser, is_staff, google_id. All personal information, medical data, and relationships will be cleared.",
        "responses": {
            200: UserSerializer,
        },
        "tags": ["User Profile"]
    }


# =============================================================================
# ADMIN USERS SCHEMAS
# =============================================================================

def admin_users_list_schema():
    return {
        "summary": "List all users",
        "description": "Retrieve a list of all users. Only accessible by administrators.",
        "tags": ["Admin - Users"]
    }

def admin_users_create_schema():
    return {
        "summary": "Create a new user",
        "description": "Create a new user account. Only accessible by administrators.",
        "tags": ["Admin - Users"]
    }

def admin_users_retrieve_schema():
    return {
        "summary": "Get user details",
        "description": "Retrieve detailed information about a specific user. Only accessible by administrators.",
        "tags": ["Admin - Users"]
    }

def admin_users_update_schema():
    return {
        "summary": "Update user (full)",
        "description": "Update all fields of a user. Only accessible by administrators.",
        "tags": ["Admin - Users"]
    }

def admin_users_partial_update_schema():
    return {
        "summary": "Update user (partial)",
        "description": "Partially update user fields. Only accessible by administrators.",
        "tags": ["Admin - Users"]
    }

def admin_users_destroy_schema():
    return {
        "summary": "Delete user",
        "description": "Delete a user account. Only accessible by administrators.",
        "tags": ["Admin - Users"]
    }


# =============================================================================
# AUTHENTICATION SCHEMAS
# =============================================================================

def register_schema():
    return {
        "summary": "Register a new user",
        "description": "Create a new user account with email, identificator, and password. The password will be hashed automatically.",
        "request": UserRegisterSerializer,
        "responses": {
            201: UserRegisterSerializer,
            400: inline_serializer(
                name="RegisterError",
                fields={
                    "email": serializers.ListField(child=serializers.CharField()),
                    "identificator": serializers.ListField(child=serializers.CharField()),
                    "password": serializers.ListField(child=serializers.CharField()),
                }
            )
        },
        "tags": ["Authentication"]
    }

def login_schema():
    return {
        "summary": "User login",
        "description": "Authenticate a user with email, identificator, and password. Returns an authentication token on success.",
        "request": inline_serializer(
            name="LoginRequest",
            fields={
                "email": serializers.EmailField(help_text="User's email address"),
                "identificator": serializers.IntegerField(help_text="User's identification number (DNI/passport)"),
                "password": serializers.CharField(help_text="User's password"),
            }
        ),
        "responses": {
            202: inline_serializer(
                name="LoginSuccessResponse",
                fields={
                    "token": serializers.CharField(help_text="Authentication token for API requests"),
                }
            ),
            401: inline_serializer(
                name="LoginErrorResponse",
                fields={
                    "error": serializers.CharField(help_text="Error message describing authentication failure"),
                }
            )
        },
        "tags": ["Authentication"]
    }

def google_login_schema():
    return {
        "summary": "Google OAuth login",
        "description": "Authenticate a user using Google OAuth. Verifies the Google ID token and creates or retrieves the user account. Returns an authentication token and user data.",
        "request": GoogleLoginSerializer,
        "responses": {
            200: inline_serializer(
                name="GoogleLoginSuccessResponse",
                fields={
                    "token": serializers.CharField(help_text="Authentication token for API requests"),
                    "user": GoogleLoginSerializer(help_text="User data"),
                }
            ),
            400: inline_serializer(
                name="GoogleLoginErrorResponse",
                fields={
                    "error": serializers.CharField(help_text="Error message (Invalid audience or Invalid token)"),
                }
            )
        },
        "tags": ["Authentication"]
    }

def password_reset_request_schema():
    return {
        "summary": "Request password reset",
        "description": "Request a password reset token. An email will be sent with the reset link.",
        "request": inline_serializer(
            name="PasswordResetRequest",
            fields={
                "email": serializers.EmailField(help_text="User's email address"),
            }
        ),
        "responses": {
            200: inline_serializer(
                name="PasswordResetRequestSuccess",
                fields={
                    "status": serializers.CharField(help_text="Status message"),
                }
            ),
            400: inline_serializer(
                name="PasswordResetRequestError",
                fields={
                    "email": serializers.ListField(child=serializers.CharField()),
                }
            )
        },
        "tags": ["Authentication"]
    }

def password_reset_confirm_schema():
    return {
        "summary": "Confirm password reset",
        "description": "Reset the password using the token received via email.",
        "request": inline_serializer(
            name="PasswordResetConfirm",
            fields={
                "token": serializers.CharField(help_text="Password reset token from email"),
                "password": serializers.CharField(help_text="New password"),
            }
        ),
        "responses": {
            200: inline_serializer(
                name="PasswordResetConfirmSuccess",
                fields={
                    "status": serializers.CharField(help_text="Status message"),
                }
            ),
            400: inline_serializer(
                name="PasswordResetConfirmError",
                fields={
                    "token": serializers.ListField(child=serializers.CharField()),
                    "password": serializers.ListField(child=serializers.CharField()),
                }
            )
        },
        "tags": ["Authentication"]
    }

def password_reset_validate_token_schema():
    return {
        "summary": "Validate password reset token",
        "description": "Validate if a password reset token is valid before showing the reset form.",
        "request": inline_serializer(
            name="PasswordResetValidateToken",
            fields={
                "token": serializers.CharField(help_text="Password reset token to validate"),
            }
        ),
        "responses": {
            200: inline_serializer(
                name="PasswordResetValidateTokenSuccess",
                fields={
                    "status": serializers.CharField(help_text="Token is valid"),
                }
            ),
            400: inline_serializer(
                name="PasswordResetValidateTokenError",
                fields={
                    "token": serializers.ListField(child=serializers.CharField()),
                }
            )
        },
        "tags": ["Authentication"]
    }


# =============================================================================
# MEDICAL OPTIONS SCHEMAS
# =============================================================================

def medical_options_list_schema():
    return {
        "summary": "Get all active medical options",
        "description": "Retrieve all active medical options (allergies, chronic diseases, previous surgeries, and disabilities) for use in forms.",
        "responses": MedicalOptionsResponseSerializer,
        "tags": ["Medical Options"]
    }


# =============================================================================
# ADMIN MEDICAL OPTIONS CRUD SCHEMAS
# =============================================================================

def medical_crud_list_schema(model_name):
    return {
        "summary": f"List all {model_name}",
        "description": f"Retrieve a list of all {model_name}. Only accessible by administrators.",
        "tags": ["Admin - Medical Options"]
    }

def medical_crud_create_schema(model_name):
    return {
        "summary": f"Create a new {model_name}",
        "description": f"Create a new {model_name} option. Only accessible by administrators.",
        "tags": ["Admin - Medical Options"]
    }

def medical_crud_retrieve_schema(model_name):
    return {
        "summary": f"Get {model_name} details",
        "description": f"Retrieve detailed information about a specific {model_name}. Only accessible by administrators.",
        "tags": ["Admin - Medical Options"]
    }

def medical_crud_update_schema(model_name):
    return {
        "summary": f"Update {model_name} (full)",
        "description": f"Update all fields of a {model_name}. Only accessible by administrators.",
        "tags": ["Admin - Medical Options"]
    }

def medical_crud_partial_update_schema(model_name):
    return {
        "summary": f"Update {model_name} (partial)",
        "description": f"Partially update {model_name} fields. Only accessible by administrators.",
        "tags": ["Admin - Medical Options"]
    }

def medical_crud_destroy_schema(model_name):
    return {
        "summary": f"Delete {model_name}",
        "description": f"Delete a {model_name} option. Only accessible by administrators.",
        "tags": ["Admin - Medical Options"]
    }

