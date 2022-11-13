from rest_framework import serializers

from acceptance.models import Acceptance
from china.serializer import ProductQuantityDetailedSerializer


class AcceptanceListSerializer(serializers.ModelSerializer):
    products = ProductQuantityDetailedSerializer(many=True, read_only=True)

    class Meta:
        model = Acceptance
        fields = '__all__'
