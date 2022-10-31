from rest_framework import serializers

from .models import LeftOver, LeftOverDetailedData
from .services import LeftOverService


_leftover_service = LeftOverService()


class LeftOverDetailSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = LeftOverDetailedData


class LeftOverSerializer(serializers.ModelSerializer):
    products = LeftOverDetailSerializer(many=True, read_only=True)

    def create(self, validated_data):
        nm = validated_data['url'].split('catalog/')[1].split('/detail')[0].strip()

        leftover_data = _leftover_service.get_leftover(nm)

        leftover = LeftOver.objects.create(
            **validated_data,
            nm=nm,
            title=leftover_data.title,
        )

        for detail in leftover_data.leftovers:
            leftover.products.create(title=detail.title, quantity=detail.quantity)

        leftover.save()

        return leftover

    class Meta:
        fields = '__all__'
        model = LeftOver
