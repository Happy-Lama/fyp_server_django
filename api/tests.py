from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from .models import TransformerData, TransformerSpecification

class TransformerModelTests(TestCase):
    def setUp(self):
        # Create TransformerSpecification instances for testing
        self.transformer_single_phase = TransformerSpecification.objects.create(
            latitude=40.7128,
            longitude=-74.0060,
            power_rating=100,
            transformer_type='SINGLE'
        )
        self.transformer_three_phase = TransformerSpecification.objects.create(
            latitude=34.0522,
            longitude=-118.2437,
            power_rating=200,
            transformer_type='THREE'
        )

    def test_transformer_specification_creation(self):
        # Test if TransformerSpecification instances are created correctly
        self.assertEqual(self.transformer_single_phase.transformer_type, 'SINGLE')
        self.assertEqual(self.transformer_three_phase.transformer_type, 'THREE')

class TransformerDataManagerTests(TestCase):
    def setUp(self):
        # Create TransformerData instances for testing
        self.transformer_off = TransformerData.objects.create(
            transformer_id=TransformerSpecification.objects.create(
                latitude=40.7128,
                longitude=-74.0060,
                power_rating=100,
                transformer_type='SINGLE'
            ),
            timestamp=timezone.now() - timedelta(minutes=40),
            status='OFF'
        )
        self.transformer_overloaded = TransformerData.objects.create(
            transformer_id=TransformerSpecification.objects.create(
                latitude=34.0522,
                longitude=-118.2437,
                power_rating=200,
                transformer_type='THREE'
            ),
            timestamp=timezone.now() - timedelta(minutes=40),
            status='OVERLOADED'
        )

    # def test_overloaded_for_period(self):
    #     # Test the overloaded_for_period method
    #     # Ensure transformer with overloaded status for more than 30 minutes is retrieved
    #     self.assertIn(self.transformer_overloaded, TransformerData.objects.overloaded_for_period(duration_minutes=30))

    def test_off_for_period(self):
        # Test the off_for_period method
        # Ensure transformer with off status for more than 30 minutes is retrieved
        selected_transformers = TransformerData.objects.off_for_period(duration_minutes=30)
        transformer_ids = [data['transformer_id'] for data in selected_transformers]
        self.assertIn(self.transformer_off.transformer_id.transformer_id, transformer_ids)

        # Ensure transformer with off status for less than 30 minutes is not retrieved
        transformer_recent_off = TransformerData.objects.create(
            transformer_id=TransformerSpecification.objects.create(
                latitude=34.0522,
                longitude=-118.2437,
                power_rating=200,
                transformer_type='THREE'
            ),
            timestamp=timezone.now() - timedelta(minutes=20),
            status='OFF'
        )

        selected_transformers = TransformerData.objects.off_for_period(duration_minutes=30)
        transformer_ids = [data['transformer_id'] for data in selected_transformers]
        self.assertNotIn(transformer_recent_off.transformer_id.transformer_id, transformer_ids)
