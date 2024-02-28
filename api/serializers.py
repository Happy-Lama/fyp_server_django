from rest_framework import serializers
from .models import TransformerData, TransformerSpecifications

class TransformerDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransformerData
        fields = '__all__'


class TransformerSpecificationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransformerSpecifications
        fields = '__all__'