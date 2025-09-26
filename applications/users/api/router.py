from rest_framework.routers import DefaultRouter
from .views import UsersAdminViewSet, UserRegisterView,UserLoginView

router = DefaultRouter()

router.register(prefix='users/admin', basename='users-admin', viewset=UsersAdminViewSet)
router.register(prefix='register', basename='users-register', viewset=UserRegisterView)
router.register(prefix='login', basename='users-login', viewset=UserLoginView)
