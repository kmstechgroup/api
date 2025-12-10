from django.views.generic import View
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from ..models import User, Allergy, ChronicDisease, PreviousSurgery, Disability
from .serializer import (
    UserRegisterSerializer, UserAdminSerializer, UserSerializer, GoogleLoginSerializer,
    AllergySerializer, ChronicDiseaseSerializer, PreviousSurgerySerializer, DisabilitySerializer,
    AllergyAdminSerializer, ChronicDiseaseAdminSerializer, PreviousSurgeryAdminSerializer, DisabilityAdminSerializer
)
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from .services import login_user, reset_user_profile
from google.oauth2 import id_token
from google.auth.transport import requests
from .swagger_schemas import (
    user_profile_schema, user_reset_profile_schema,
    admin_users_list_schema, admin_users_create_schema, admin_users_retrieve_schema,
    admin_users_update_schema, admin_users_partial_update_schema, admin_users_destroy_schema,
    register_schema, login_schema, google_login_schema,
    medical_options_list_schema,
    medical_crud_list_schema, medical_crud_create_schema, medical_crud_retrieve_schema,
    medical_crud_update_schema, medical_crud_partial_update_schema, medical_crud_destroy_schema
)




class UserViewSet(ViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(**user_profile_schema())
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

    @extend_schema(**user_reset_profile_schema())
    @action(detail=False, methods=["patch"])
    def reset_profile(self, request):
        """Reset user profile data to null, keeping only essential fields."""
        reset_user_profile(request.user)
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UsersAdminViewSet(ModelViewSet):
    """
    ViewSet for admin operations on users.
    Provides full CRUD operations for user management.
    Only accessible by administrators.
    """
    queryset = User.objects.all()
    serializer_class = UserAdminSerializer
    permission_classes = [IsAdminUser]
    
    @extend_schema(**admin_users_list_schema())
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @extend_schema(**admin_users_create_schema())
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @extend_schema(**admin_users_retrieve_schema())
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @extend_schema(**admin_users_update_schema())
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @extend_schema(**admin_users_partial_update_schema())
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    @extend_schema(**admin_users_destroy_schema())
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
class UserRegisterView(ViewSet):
    permission_classes = [AllowAny]
    
    @extend_schema(**register_schema())
    def create(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserLoginView(ViewSet):
    permission_classes = [AllowAny]
    
    @extend_schema(**login_schema())
    def create(self, request):
        user = login_user(email=request.data['email'], password=request.data['password'], identificator=request.data['identificator'])
        print(f"User:{user}")
        if 'error' in user:
            return Response(user, status=status.HTTP_401_UNAUTHORIZED)
        
        return Response(user, status=status.HTTP_202_ACCEPTED)
    
    
class UserGoogleLoginSet(ViewSet):
    permission_classes = [AllowAny]
    serializer_class = GoogleLoginSerializer
    
    @extend_schema(**google_login_schema())
    def create(self, request):
        serializer = GoogleLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        identificator = serializer.validated_data["identificator"]
        token = serializer.validated_data["id_token"]
        identificator = serializer.validated_data["identificator"]
        try:
            # Verify token with Google
            idinfo = id_token.verify_oauth2_token(token, requests.Request())

            # Validate the aud (client_id of your app in Google Cloud)
            if idinfo["aud"] != "324154317577-fg88npuvs4d57nku05fs7ubcte2dbdro.apps.googleusercontent.com":
                return Response(
                    {"error": "Invalid audience"}, status=status.HTTP_400_BAD_REQUEST
                )

            email = idinfo.get("email")
            first_name = idinfo.get("given_name")
            last_name = idinfo.get("family_name")
            
            # Find or create user
            user, created = User.objects.get_or_create(
            email=email,
            defaults={
                "identificator": identificator,
                "first_name": first_name,
                "last_name": last_name,
            },
        )


            # Generate internal token
            token_obj, _ = Token.objects.get_or_create(user=user)

            # Serialize user for response
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

    @extend_schema(**medical_options_list_schema())
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


# =============================================================================
# ADMIN CRUD VIEWSETS FOR MEDICAL OPTIONS
# =============================================================================

class AllergyViewSet(ModelViewSet):
    """
    ViewSet for admin CRUD operations on Allergy model.
    Only accessible by administrators.
    """
    queryset = Allergy.objects.all()
    serializer_class = AllergyAdminSerializer
    permission_classes = [IsAdminUser]
    
    @extend_schema(**medical_crud_list_schema("allergies"))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @extend_schema(**medical_crud_create_schema("allergies"))
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @extend_schema(**medical_crud_retrieve_schema("allergies"))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @extend_schema(**medical_crud_update_schema("allergies"))
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @extend_schema(**medical_crud_partial_update_schema("allergies"))
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    @extend_schema(**medical_crud_destroy_schema("allergies"))
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class ChronicDiseaseViewSet(ModelViewSet):
    """
    ViewSet for admin CRUD operations on ChronicDisease model.
    Only accessible by administrators.
    """
    queryset = ChronicDisease.objects.all()
    serializer_class = ChronicDiseaseAdminSerializer
    permission_classes = [IsAdminUser]
    
    @extend_schema(**medical_crud_list_schema("chronic diseases"))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @extend_schema(**medical_crud_create_schema("chronic diseases"))
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @extend_schema(**medical_crud_retrieve_schema("chronic diseases"))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @extend_schema(**medical_crud_update_schema("chronic diseases"))
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @extend_schema(**medical_crud_partial_update_schema("chronic diseases"))
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    @extend_schema(**medical_crud_destroy_schema("chronic diseases"))
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class PreviousSurgeryViewSet(ModelViewSet):
    """
    ViewSet for admin CRUD operations on PreviousSurgery model.
    Only accessible by administrators.
    """
    queryset = PreviousSurgery.objects.all()
    serializer_class = PreviousSurgeryAdminSerializer
    permission_classes = [IsAdminUser]
    
    @extend_schema(**medical_crud_list_schema("previous surgeries"))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @extend_schema(**medical_crud_create_schema("previous surgeries"))
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @extend_schema(**medical_crud_retrieve_schema("previous surgeries"))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @extend_schema(**medical_crud_update_schema("previous surgeries"))
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @extend_schema(**medical_crud_partial_update_schema("previous surgeries"))
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    @extend_schema(**medical_crud_destroy_schema("previous surgeries"))
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class DisabilityViewSet(ModelViewSet):
    """
    ViewSet for admin CRUD operations on Disability model.
    Only accessible by administrators.
    """
    queryset = Disability.objects.all()
    serializer_class = DisabilityAdminSerializer
    permission_classes = [IsAdminUser]
    
    @extend_schema(**medical_crud_list_schema("disabilities"))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @extend_schema(**medical_crud_create_schema("disabilities"))
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @extend_schema(**medical_crud_retrieve_schema("disabilities"))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @extend_schema(**medical_crud_update_schema("disabilities"))
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @extend_schema(**medical_crud_partial_update_schema("disabilities"))
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    @extend_schema(**medical_crud_destroy_schema("disabilities"))
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)