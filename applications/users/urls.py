from django.urls import path, include
from .api.router import router_users

urlpatterns = [
    path('', include(router_users.urls)),
]
