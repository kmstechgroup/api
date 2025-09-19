from django.urls import path, include
from rest_framework import routers
#from .api import UserViewSet
from .api.views import UsersAPIView

router = routers.DefaultRouter()

#router.register('api/users', UserViewSet, 'users')
urlpatterns = [#router.urls,
               path('api/users/', UsersAPIView.as_view(), name='user_list'),
               path('api/users/<int:pk>/', UsersAPIView.as_view(), name='user_id'),
            ]


