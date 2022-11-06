from rest_framework import serializers

from .models import LeftOver, LeftOverDetailedData
from .services import get_leftover


class CustomSerializer(serializers.HyperlinkedModelSerializer):

    def get_field_names(self, declared_fields, info):
        expanded_fields = super(CustomSerializer, self).get_field_names(declared_fields, info)

        if getattr(self.Meta, 'extra_fields', None):
            return expanded_fields + self.Meta.extra_fields
        else:
            return expanded_fields


class LeftOverDetailSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = LeftOverDetailedData


class LeftOverSerializer(serializers.ModelSerializer):
    products = LeftOverDetailSerializer(many=True, read_only=True)
    buffer = LeftOverDetailSerializer(many=True, read_only=True)
    sorted_buffer = serializers.SerializerMethodField()
    sorted_products = serializers.SerializerMethodField()

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

    def get_sorted_buffer(self, obj):
        return LeftOverDetailSerializer(sorted(
            obj.buffer.all(),
            key=lambda x: x.title.split('/')[0]
        ), many=True, read_only=True).data

    def get_sorted_products(self, obj):
        return LeftOverDetailSerializer(sorted(
            obj.products.all(),
            key=lambda x: x.title.split('/')[0]
        ), many=True, read_only=True).data

    class Meta:
        fields = ('id', 'sorted_products', 'sorted_buffer', 'total', 'buffer_total', 'title', 'url', 'photo_url', 'nm',
                  'buffer', 'products')
        model = LeftOver
