# =============================================================================
# API ROUTER CONFIGURATION
# =============================================================================

from rest_framework.routers import DefaultRouter
from .views import DepartmentViewSet

# Create the main router instance
router = DefaultRouter()

# =============================================================================
# ROUTE REGISTRATIONS
# =============================================================================

router.register(r'backoffice/departments', DepartmentViewSet, basename='departments-admin')
