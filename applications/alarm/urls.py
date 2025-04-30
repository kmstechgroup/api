from django.urls import path, include
from rest_framework import routers
from .api import EmergencyViewSet, CommunicateEmergencyDepartmentViewSet


router = routers.DefaultRouter()

router.register('api/emergencys', EmergencyViewSet, 'emergencys')
router.register('api/emergency_department', CommunicateEmergencyDepartmentViewSet, 'emergency_department')

urlpatterns = router.urls