from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import TransformerData, TransformerSpecification, TransformerDataManager
from notifications.models import Notification
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

@receiver(post_save, sender=TransformerData)
def create_notification(sender, instance, created, **kwargs):
    if created:
        # Create a notification (warning level) if the saved values are above the threshold
        # Create a notification (danger level) if the transformer has gone offline
        # Broadcast new data to the users via a websocket
        print("TransformerData Saved")
        TransformerDataManager().check_thresholds(instance, Notification)
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)('users', {'type': 'send_notification', 'message': 'new_transformer_data'})
        
@receiver(post_save, sender=TransformerSpecification)
def transformer_registered_notification(sender, instance, created, **kwargs):
    if created:
        # Create a notification (info level) that a transformer module has been registered
        # Broadcast information to the users via a websocket
        print("TransformerSpecification Saved")
        