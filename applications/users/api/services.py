from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

#Login Logic
def login_user(email: str, identificator: int, password: str):
    """
    This try authenticate with email, identificator and password. If that fail send a error. If works send the token.
    """
    user = authenticate(email=email, identificator=identificator, password=password)
    if not user:
        return {"error": "Invalid credentials"}

    token, created = Token.objects.get_or_create(user=user)
    return {"token": token.key}