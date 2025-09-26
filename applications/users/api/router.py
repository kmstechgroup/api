from rest_framework.routers import DefaultRouter
from .views import UsersAdminViewSet, UserRegisterView,UserLoginView,UserViewSet

router = DefaultRouter()

router.register(prefix='backoffice/users', basename='users-admin', viewset=UsersAdminViewSet)
router.register(prefix='register', basename='users-register', viewset=UserRegisterView)
router.register(prefix='login', basename='users-login', viewset=UserLoginView)
router.register(prefix='user', basename='users-profile', viewset=UserViewSet)
