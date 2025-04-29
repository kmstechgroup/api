from django.urls import path, include
from rest_framework import routers
from .api import DepartmentViewSet


router = routers.DefaultRouter()

router.register('api/departments', DepartmentViewSet, 'Departments')




urlpatterns = router.urls