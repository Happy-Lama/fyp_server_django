from django.db import models
from django.utils import timezone
from datetime import timedelta
# from notifications.models import Notification
# model managers

class TransformerDataManager(models.Manager):
    # def overloaded_for_period(self, duration_minutes=30):
    #     # transformers that have been overloaded for a certain period of time or more
    #     # latest state change for each transformer
    #     latest_status_changes = self.get_queryset().values('transformer_id').annotate(
    #         latest_change = models.Max('timestamp')
    #     )

    #     # retrieve previous status for each transformer
    #     previous_status_changes = latest_status_changes.annotate(
    #         previous_status= models.Lag('status')
    #     )
    #     pass

    def off_for_period(self, duration_minutes=30):
        # transformers that have been off for a long time

        # get latest transformer off status
        latest_off_status_changes = self.get_queryset().filter(
            status='OFF'
        ).values('transformer_id').annotate(
            latest_change = models.Max('timestamp')
        )

        # filter for those that have been off  30 minutes or more
        selected_transformers = latest_off_status_changes.filter(
            latest_change__lte=timezone.now() - timedelta(minutes=duration_minutes)
        )

        return selected_transformers
    
    def check_thresholds(self, transformer_data_instance, notification_class):

        transformer_spec = transformer_data_instance.transformer_id

        # Check loading threshold
        loading_threshold = transformer_spec.power_rating * 0.9  # Example threshold: 80% of power rating
        total_power = transformer_data_instance.out_pa + transformer_data_instance.out_pb + transformer_data_instance.out_pc
        if total_power > loading_threshold:
            message = f"Transformer {transformer_spec.transformer_id} exceeded loading threshold."
            self.create_notification(transformer_spec, message, 'DANGER', notification_class)

        # Check phase voltage threshold
        phase_voltage_threshold = 240  # Example threshold: 240V
        if not ((phase_voltage_threshold * 0.94 <= transformer_data_instance.out_ua <= phase_voltage_threshold * 1.06) or
                (phase_voltage_threshold * 0.94 <= transformer_data_instance.out_ub <= phase_voltage_threshold * 1.06) or
                (phase_voltage_threshold * 0.94 <= transformer_data_instance.out_uc <= phase_voltage_threshold * 1.06)):
            message = f"Transformer {transformer_spec.transformer_id} exceeded phase voltage threshold."
            self.create_notification(transformer_spec, message, 'WARN', notification_class)

        # Check frequency threshold
        frequency_threshold = 50  # Example threshold: 50Hz
        if not (frequency_threshold - 0.5 <= transformer_data_instance.out_freq <= frequency_threshold + 0.5):
            message = f"Transformer {transformer_spec.transformer_id} frequency is not within threshold."
            self.create_notification(transformer_spec, message, 'WARN', notification_class)

    def create_notification(self, transformer_spec, message, notification_type, notification_class):
        notification_class.objects.create(
            transformer_id=transformer_spec,
            message=message,
            notification_type=notification_type
        )

# models
class TransformerSpecification(models.Model):
    # Transformer specifications model

    transformer_types = [
        ('SINGLE', 'SINGLE PHASE TRANSFORMER'),
        ('THREE', 'THREE PHASE TRANSFORMER'),
    ]

    transformer_id = models.CharField(primary_key=True, max_length=256)
    latitude = models.FloatField()
    longitude = models.FloatField()
    power_rating = models.PositiveBigIntegerField(default=100)
    transformer_type = models.CharField(max_length=6, choices=transformer_types)


    


class TransformerData(models.Model):
    # transformer data model

    transformer_status = [
        ('ON', 'Transformer Online'),
        ('OFF', 'Transformer Offline'),
        ('OVERLOADED', 'Transformer Overloaded'),
    ]


    
    transformer_id = models.ForeignKey(TransformerSpecification, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)

    # output phase voltages
    out_ua = models.FloatField(default=0)
    out_ub = models.FloatField(default=0)
    out_uc = models.FloatField(default=0)

    # output phase currents
    out_ia = models.FloatField(default=0)
    out_ib = models.FloatField(default=0)
    out_ic = models.FloatField(default=0)

    # output line to line voltages
    out_uab = models.FloatField(default=0)
    out_ubc = models.FloatField(default=0)
    out_uca = models.FloatField(default=0)

    # output active phase power
    out_pa = models.FloatField(default=0)
    out_pb = models.FloatField(default=0)
    out_pc = models.FloatField(default=0)

    # output reactive phase power
    out_qa = models.FloatField(default=0)
    out_qb = models.FloatField(default=0)
    out_qc = models.FloatField(default=0)

    # output apparent phase power
    out_sa = models.FloatField(default=0)
    out_sb = models.FloatField(default=0)
    out_sc = models.FloatField(default=0)

    # output power factor per phase
    # out_pha = models.FloatField(default=0)
    # out_phb = models.FloatField(default=0)
    # out_phc = models.FloatField(default=0)

    # output frequency
    out_freq = models.FloatField(default=0)

    status = models.CharField(default='ON', choices=transformer_status, max_length=15)
    
    objects = TransformerDataManager()



