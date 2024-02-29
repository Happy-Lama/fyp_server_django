from django.db import models
from django.utils import timezone
from api.models import TransformerSpecification


class Notification(models.Model):
    # Notifications model
    
    notification_types = [
        ('WARN', 'WARNING'),
        ('DANGER', 'DANGER'),
        ('INFO', 'INFORMATIONAL'),
        # ('SUCCESS', 'TRANSFORMER BACK TO NORMAL BEHAVIOUR'),
    ]
    transformer_id = models.ForeignKey(TransformerSpecification, on_delete=models.SET_NULL, null=True, blank=True, default=None)
    message = models.CharField(max_length=255)
    notification_type = models.CharField(max_length=7, choices=notification_types)
    timestamp = models.DateTimeField(default=timezone.now)