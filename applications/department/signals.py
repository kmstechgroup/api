# =============================================================================
# DEPARTMENT SIGNALS
# =============================================================================

from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Department


@receiver(pre_save, sender=Department)
def calculate_expanded_jurisdiction(sender, instance, **kwargs):
    """
    Automatically calculates jurisdiction_expanded as a 1km buffer
    around jurisdiction before saving.
    
    This signal automatically executes every time a Department is saved or updated,
    calculating the expanded jurisdiction based on the original jurisdiction.
    """
    if instance.jurisdiction:
        # Create a 1 kilometer buffer around the polygon
        # buffer() receives the distance in meters (1000 = 1km)
        instance.jurisdiction_expanded = instance.jurisdiction.buffer(1000)
    else:
        # If there is no jurisdiction, there is no expanded one either
        instance.jurisdiction_expanded = None
