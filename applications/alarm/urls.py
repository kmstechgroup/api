from django.urls import path, include
from rest_framework import routers
from .api import EmergencyViewSet, CommunicateEmergencyDepartmentViewSet


router = routers.DefaultRouter()

router.register('api/emergencys', EmergencyViewSet, 'emergencys')
router.register('api/emergencys_departmets', CommunicateEmergencyDepartmentViewSet, 'emergency_departments')

urlpatterns = router.urls