from django.urls import path, include
from .api.router import router

urlpatterns = [
    path('', include(router.urls)),
    path('auth/password-reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
]
