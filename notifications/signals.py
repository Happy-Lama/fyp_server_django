from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Notification

@receiver(post_save, sender=Notification)
def broadcast_notification(sender, instance, created, **kwargs):
    if created:
        # Broadcast the notification on the users channel
        print("Notification Created")
        pass