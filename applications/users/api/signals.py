# =============================================================================
# PASSWORD RESET SIGNALS
# =============================================================================

from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django_rest_passwordreset.signals import reset_password_token_created, post_password_reset
from rest_framework.authtoken.models import Token


@receiver(reset_password_token_created)
def password_reset_token_created_handler(sender, instance, reset_password_token, **kwargs):
    """
    Signal handler that executes when a password reset token is created.
    Sends an email to the user with the link to reset their password.
    """
    # Build app deep link URL with the token
    # Custom URL scheme format: safeon://reset-password?token=...
    # Configuration comes from .env file: APP_SCHEME
    reset_url = f"{settings.APP_SCHEME}://reset-password?token={reset_password_token.key}"
    
    # Build email message
    subject = "Restablecer contraseña - SafeOn"
    
    message = f"""
Hola {reset_password_token.user.first_name or 'Usuario'},

Has solicitado restablecer tu contraseña en SafeOn.

Haz clic en el siguiente enlace para continuar:
{reset_url}

Este enlace no expira, pero solo puede usarse una vez.

Si no solicitaste este cambio, ignora este email y tu contraseña permanecerá sin cambios.

Saludos,
El equipo de SafeOn
"""
    
    # Send email
    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'SafeOn <noreply@safeon.com>')
    
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=[reset_password_token.user.email],
            fail_silently=False,
        )
    except Exception as e:
        # Log error if necessary
        print(f"Error sending password reset email: {e}")


@receiver(post_password_reset)
def post_password_reset_handler(sender, user, **kwargs):
    """
    Signal handler that executes after the user resets their password.
    Deletes the current authentication token to force a new login.
    """
    # Delete current authentication token
    # This forces the user to login again with the new password
    Token.objects.filter(user=user).delete()

