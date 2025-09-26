from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class EmailIdentificatorBackend(ModelBackend):
    def authenticate(self, request, username=None, email=None, identificator=None, password=None, **kwargs):
        # Admin manda "username", lo usamos como email
        if email is None:
            email = username

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return None

        # 🔐 Caso admin/superuser → solo email + password
        if user.is_staff or user.is_superuser:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
            return None

        # 🔐 Caso usuario común → necesita identificator válido
        if identificator is None:
            return None  # si no mandó identificator, rechazamos

        if str(user.identificator) != str(identificator):
            return None  # si no coincide, rechazamos

        if user.check_password(password) and self.user_can_authenticate(user):
            return user

        return None
