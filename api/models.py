from django.db import models
from django.utils import timezone
from datetime import timedelta

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



