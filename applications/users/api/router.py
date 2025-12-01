# =============================================================================
# API ROUTER CONFIGURATION
# =============================================================================

from rest_framework.routers import DefaultRouter
from .views import UsersAdminViewSet, UserRegisterView, UserLoginView, UserViewSet, UserGoogleLoginSet, MedicalOptionsViewSet

# Create the main router instance
router = DefaultRouter()

# =============================================================================
# ROUTE REGISTRATIONS
# =============================================================================

# Admin routes - Full CRUD operations for administrators
router.register(
    prefix='backoffice/users', 
    basename='users-admin', 
    viewset=UsersAdminViewSet
)

# Authentication routes - Public access
router.register(
    prefix='register', 
    basename='users-register', 
    viewset=UserRegisterView
)

router.register(
    prefix='auth/login', 
    basename='users-login', 
    viewset=UserLoginView
)

router.register(
    prefix='auth/google', 
    basename='users-google', 
    viewset=UserGoogleLoginSet
)

# User profile routes - Authenticated users only
router.register(
    prefix='user', 
    basename='users-profile', 
    viewset=UserViewSet
)

# Medical options routes - Authenticated users only
router.register(
    prefix='medical-options', 
    basename='medical-options', 
    viewset=MedicalOptionsViewSet
)
