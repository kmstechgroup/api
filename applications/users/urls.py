from django.urls import path, include
from drf_spectacular.utils import extend_schema_view, extend_schema
from django_rest_passwordreset.views import (
    ResetPasswordRequestTokenViewSet,
    ResetPasswordConfirmViewSet,
    ResetPasswordValidateTokenViewSet
)
from .api.router import router
from .api.swagger_schemas import (
    password_reset_request_schema,
    password_reset_confirm_schema,
    password_reset_validate_token_schema
)

# Extend password reset ViewSets with Authentication tag
ResetPasswordRequestTokenViewSet = extend_schema_view(
    create=extend_schema(**password_reset_request_schema())
)(ResetPasswordRequestTokenViewSet)

ResetPasswordConfirmViewSet = extend_schema_view(
    create=extend_schema(**password_reset_confirm_schema())
)(ResetPasswordConfirmViewSet)

ResetPasswordValidateTokenViewSet = extend_schema_view(
    create=extend_schema(**password_reset_validate_token_schema())
)(ResetPasswordValidateTokenViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # Password reset endpoints with Authentication tag
    path('auth/password-reset/', ResetPasswordRequestTokenViewSet.as_view({'post': 'create'}), name='reset-password-request'),
    path('auth/password-reset/confirm/', ResetPasswordConfirmViewSet.as_view({'post': 'create'}), name='reset-password-confirm'),
    path('auth/password-reset/validate_token/', ResetPasswordValidateTokenViewSet.as_view({'post': 'create'}), name='reset-password-validate'),
]
