import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fyp_server.settings")

# Call django.setup() to initialize Django
django.setup()

from datetime import timedelta
import random
from django.utils import timezone
from api.models import TransformerSpecification, TransformerData
from django.db import transaction

# # Set the DJANGO_SETTINGS_MODULE environment variable


def generate_transformer_data():
    # Create TransformerSpecifications
    transformer_specs = []
    for i in range(4):
        transformer = TransformerSpecification.objects.create(
            latitude=random.uniform(-90, 90),
            longitude=random.uniform(-180, 180),
            power_rating=random.randint(50, 500),
            transformer_type=random.choice(['SINGLE', 'THREE'])
        )
        transformer_specs.append(transformer)

    # Generate TransformerData for each TransformerSpecification
    start_time = timezone.now() - timedelta(days=7)
    end_time = timezone.now()
    with transaction.atomic():
        for _ in range(100):
            transformer_spec = random.choice(transformer_specs)
            timestamp = timezone.localtime(start_time + timedelta(days=random.randint(0, 6), hours=random.randint(0, 23), minutes=random.randint(0, 59)))
            TransformerData.objects.create(
                transformer_id=transformer_spec,
                timestamp=timestamp,
                out_ua=random.uniform(100, 250),
                out_ub=random.uniform(100, 250),
                out_uc=random.uniform(100, 250),
                out_ia=random.uniform(5, 50),
                out_ib=random.uniform(5, 50),
                out_ic=random.uniform(5, 50),
                out_uab=random.uniform(150, 300),
                out_ubc=random.uniform(150, 300),
                out_uca=random.uniform(150, 300),
                out_pa=random.uniform(500, 1000),
                out_pb=random.uniform(500, 1000),
                out_pc=random.uniform(500, 1000),
                out_qa=random.uniform(200, 500),
                out_qb=random.uniform(200, 500),
                out_qc=random.uniform(200, 500),
                out_sa=random.uniform(600, 1200),
                out_sb=random.uniform(600, 1200),
                out_sc=random.uniform(600, 1200),
                out_freq=random.uniform(49, 51),
                status=random.choice(['ON', 'OFF', 'OVERLOADED'])
            )

if __name__ == "__main__":
    generate_transformer_data()
