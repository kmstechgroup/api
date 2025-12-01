from django.views.generic import View
from drf_spectacular.utils import extend_schema, OpenApiParameter,inline_serializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from ..models import User, Allergy, ChronicDisease, PreviousSurgery, Disability
from .serializer import UserRegisterSerializer, UserAdminSerializer, UserSerializer, GoogleLoginSerializer, AllergySerializer, ChronicDiseaseSerializer, PreviousSurgerySerializer, DisabilitySerializer, MedicalOptionsResponseSerializer
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework import serializers
from .services import login_user
from google.oauth2 import id_token
from google.auth.transport import requests




class UserViewSet(ViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Get or update user profile",
        description="GET: Retrieve the authenticated user's profile information including personal data, medical information, and emergency contacts. PATCH: Update the authenticated user's profile information. Only provided fields will be updated (partial update).",
        request=UserSerializer,
        responses={
            200: UserSerializer,
            400: inline_serializer(
                name="ProfileUpdateError",
                fields={
                    "field_name": serializers.ListField(child=serializers.CharField()),
                }
            )
        },
        tags=["User Profile"]
    )
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
    """
    ViewSet for admin operations on users.
    Provides full CRUD operations for user management.
    Only accessible by administrators.
    """
    queryset = User.objects.all()
    serializer_class = UserAdminSerializer
    permission_classes = [IsAdminUser]
    
    @extend_schema(
        summary="List all users",
        description="Retrieve a list of all users. Only accessible by administrators.",
        tags=["Admin - Users"]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @extend_schema(
        summary="Create a new user",
        description="Create a new user account. Only accessible by administrators.",
        tags=["Admin - Users"]
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @extend_schema(
        summary="Get user details",
        description="Retrieve detailed information about a specific user. Only accessible by administrators.",
        tags=["Admin - Users"]
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @extend_schema(
        summary="Update user (full)",
        description="Update all fields of a user. Only accessible by administrators.",
        tags=["Admin - Users"]
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @extend_schema(
        summary="Update user (partial)",
        description="Partially update user fields. Only accessible by administrators.",
        tags=["Admin - Users"]
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    @extend_schema(
        summary="Delete user",
        description="Delete a user account. Only accessible by administrators.",
        tags=["Admin - Users"]
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
class UserRegisterView(ViewSet):
    permission_classes = [AllowAny]
    
    @extend_schema(
        summary="Register a new user",
        description="Create a new user account with email, identificator, and password. The password will be hashed automatically.",
        request=UserRegisterSerializer,
        responses={
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
        tags=["Authentication"]
    )
    def create(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserLoginView(ViewSet):
    permission_classes = [AllowAny]
    
    @extend_schema(
        summary="User login",
        description="Authenticate a user with email, identificator, and password. Returns an authentication token on success.",
        request=inline_serializer(
            name="LoginRequest",
            fields={
                "email": serializers.EmailField(help_text="User's email address"),
                "identificator": serializers.IntegerField(help_text="User's identification number (DNI/passport)"),
                "password": serializers.CharField(help_text="User's password"),
            }
        ),
        responses={
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
        tags=["Authentication"]
    )
    def create(self, request):
        user = login_user(email=request.data['email'], password=request.data['password'], identificator=request.data['identificator'])
        print(f"User:{user}")
        if 'error' in user:
            return Response(user, status=status.HTTP_401_UNAUTHORIZED)
        
        return Response(user, status=status.HTTP_202_ACCEPTED)
    
    
class UserGoogleLoginSet(ViewSet):
    permission_classes = [AllowAny]
    serializer_class = GoogleLoginSerializer
    
    @extend_schema(
        summary="Google OAuth login",
        description="Authenticate a user using Google OAuth. Verifies the Google ID token and creates or retrieves the user account. Returns an authentication token and user data.",
        request=GoogleLoginSerializer,
        responses={
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
        tags=["Authentication"]
    )
    def create(self, request):
        serializer = GoogleLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        identificator = serializer.validated_data["identificator"]
        token = serializer.validated_data["id_token"]
        identificator = serializer.validated_data["identificator"]
        try:
            # ✅ Verificar token con Google
            idinfo = id_token.verify_oauth2_token(token, requests.Request())

            # Validar el aud (client_id de tu app en Google Cloud)
            if idinfo["aud"] != "324154317577-fg88npuvs4d57nku05fs7ubcte2dbdro.apps.googleusercontent.com":
                return Response(
                    {"error": "Invalid audience"}, status=status.HTTP_400_BAD_REQUEST
                )

            email = idinfo.get("email")
            first_name = idinfo.get("given_name")
            last_name = idinfo.get("family_name")
            
            # Buscar o crear usuario
            user, created = User.objects.get_or_create(
            email=email,
            defaults={
                "identificator": identificator,
                "first_name": first_name,
                "last_name": last_name,
            },
        )


            # Generar token interno
            token_obj, _ = Token.objects.get_or_create(user=user)

            # Serializar usuario para la respuesta
            response_serializer = self.serializer_class(user)

            return Response(
                {
                    "token": token_obj.key,
                    "user": response_serializer.data,
                },
                status=status.HTTP_200_OK,
            )

        except ValueError:
            return Response(
                {"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST
            )


class MedicalOptionsViewSet(ViewSet):
    """
    ViewSet to retrieve all active medical options.
    Returns allergies, chronic diseases, previous surgeries, and disabilities.
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Get all active medical options",
        description="Retrieve all active medical options (allergies, chronic diseases, previous surgeries, and disabilities) for use in forms.",
        responses=MedicalOptionsResponseSerializer,
        tags=["Medical Options"]
    )
    def list(self, request):
        """
        Retrieve all active medical options.
        Returns a dictionary with all medical option types.
        """
        allergies = Allergy.objects.filter(is_active=True)
        chronic_diseases = ChronicDisease.objects.filter(is_active=True)
        previous_surgeries = PreviousSurgery.objects.filter(is_active=True)
        disabilities = Disability.objects.filter(is_active=True)

        allergies_serializer = AllergySerializer(allergies, many=True)
        chronic_diseases_serializer = ChronicDiseaseSerializer(chronic_diseases, many=True)
        previous_surgeries_serializer = PreviousSurgerySerializer(previous_surgeries, many=True)
        disabilities_serializer = DisabilitySerializer(disabilities, many=True)

        return Response({
            "allergies": allergies_serializer.data,
            "chronic_diseases": chronic_diseases_serializer.data,
            "previous_surgeries": previous_surgeries_serializer.data,
            "disabilities": disabilities_serializer.data,
        })