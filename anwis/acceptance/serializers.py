from rest_framework import serializers

from acceptance.models import Acceptance, StaffMember, AcceptanceCategory, Product
from china.serializer import ProductQuantityDetailedSerializer


class AcceptanceListSerializer(serializers.ModelSerializer):
    products = ProductQuantityDetailedSerializer(many=True, read_only=True)

    class Meta:
        model = Acceptance
        fields = '__all__'


class AcceptanceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Acceptance
        fields = '__all__'


class StaffMemberSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = StaffMember


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = AcceptanceCategory


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
