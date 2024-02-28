from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import TransformerData, TransformerSpecification
from notifications.models import Notification

@receiver(post_save, sender=TransformerData)
def create_notification(sender, instance, created, **kwargs):
    if created:
        # Create a notification (warning level) if the saved values are above the threshold
        # Create a notification (danger level) if the transformer has gone offline
        # Broadcast new data to the users via a websocket
        print("TransformerData Saved")
        pass

@receiver(post_save, sender=TransformerSpecification)
def transformer_registered_notification(sender, instance, created, **kwargs):
    if created:
        # Create a notification (info level) that a transformer module has been registered
        # Broadcast information to the users via a websocket
        print("TransformerSpecification Saved")
        pass