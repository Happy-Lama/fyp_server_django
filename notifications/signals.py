from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Notification
from firebase import send_notification_to_all_users
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

@receiver(post_save, sender=Notification)
def broadcast_notification(sender, instance, created, **kwargs):
    if created:
        # Broadcast the notification on the users channel
        print("Notification Created")
        if instance.notification_type in ['DANGER', 'INFO']:
            send_notification_to_all_users(title=instance.notification_type, body=f'{instance.message} : Transformer {instance.transformer_id}, Timestamp : {instance.timestamp}')
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)('users', {'type': 'send_notification', 'message': 'new_notification'})