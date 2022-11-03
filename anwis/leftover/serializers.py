from rest_framework import serializers

from .models import LeftOver, LeftOverDetailedData
from .services import get_leftover


class LeftOverDetailSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = LeftOverDetailedData


class LeftOverSerializer(serializers.ModelSerializer):
    products = LeftOverDetailSerializer(many=True, read_only=True)
    buffer = LeftOverDetailSerializer(many=True, read_only=True)

    def create(self, validated_data):
        nm = validated_data['url'].split('catalog/')[1].split('/detail')[0].strip()

        leftover_data = get_leftover(nm)

        leftover = LeftOver.objects.create(
            **validated_data,
            nm=nm,
            title=leftover_data.title,
        )

        total = 0

        for detail in leftover_data.leftovers:
            total += detail.quantity
            leftover.products.create(title=detail.title, quantity=detail.quantity)

        leftover.total = total

        leftover.save()

        return leftover

    class Meta:
        fields = '__all__'
        model = LeftOver
