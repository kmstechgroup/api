# =============================================================================
# AUTHENTICATION SERVICES
# =============================================================================

from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from ..models import User


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


def reset_user_profile(user: User) -> User:
    """
    Reset user profile data to null, keeping only essential fields.
    Preserves: id, password, email, identificator, is_active, last_login, 
    date_joined, is_oauth_user, is_superuser, is_staff, google_id
    
    Args:
        user (User): User instance to reset
        
    Returns:
        User: The reset user instance
    """
    # Clear all ManyToMany relationships
    user.allergies.clear()
    user.chronic_diseases.clear()
    user.previous_surgeries.clear()
    user.disabilities.clear()
    
    # Set all other fields to null/empty (except preserved fields)
    # Note: first_name and last_name from AbstractUser cannot be None, use empty string
    user.username = None  # Can be None (has null=True in model)
    user.first_name = ''  # Cannot be None (AbstractUser field)
    user.last_name = ''   # Cannot be None (AbstractUser field)
    user.address = None
    user.blood_type = None
    user.sex = None
    user.height = None
    user.weight = None
    user.birthdate = None
    user.allergies_other = None
    user.chronic_diseases_other = None
    user.previous_surgeries_other = None
    user.disabilities_other = None
    user.close_contacts = {}
    user.phone_number = None
    user.strikes = 0
    user.blocked = False
    
    user.save()
    return user