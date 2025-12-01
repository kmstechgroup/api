from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class EmailIdentificatorBackend(ModelBackend):
    def authenticate(self, request, username=None, email=None, identificator=None, password=None, **kwargs):
        # Admin sends "username", we use it as email
        if email is None:
            email = username

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return None

        # 🔐 Admin/superuser case → only email + password
        if user.is_staff or user.is_superuser:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
            return None

        # 🔐 Common user case → needs valid identificator
        if identificator is None:
            return None  # if no identificator provided, reject

        if str(user.identificator) != str(identificator):
            return None  # if doesn't match, reject

        if user.check_password(password) and self.user_can_authenticate(user):
            return user

        return None
