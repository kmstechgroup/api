# =============================================================================
# AUTHENTICATION SERVICES
# =============================================================================

from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token


def login_user(email: str, identificator: int, password: str):
    """
    Authenticate user with email, identificator, and password.
    
    Args:
        email (str): User's email address
        identificator (int): User's identification number
        password (str): User's password
        
    Returns:
        dict: Either {"token": "token_key"} on success or {"error": "message"} on failure
        
    This function attempts to authenticate a user using Django's built-in
    authentication system. If authentication fails, it returns an error message.
    If successful, it creates or retrieves an authentication token for the user.
    """
    
    # Attempt to authenticate user with provided credentials
    user = authenticate(email=email, identificator=identificator, password=password)
    
    # Return error if authentication fails
    if not user:
        return {"error": "Invalid credentials"}

    # Create or get existing token for authenticated user
    token, created = Token.objects.get_or_create(user=user)
    return {"token": token.key}