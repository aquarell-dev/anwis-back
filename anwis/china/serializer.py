from rest_framework import serializers

from .models import ChinaDistributor, Product, OrderForProject, Order, Status, IndividualEntrepreneur


class ChinaSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = ChinaDistributor


class OrderForProjectSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = OrderForProject


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Status


class IndividualEntrepreneurSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = IndividualEntrepreneur


class OrderListRetrieveSerializer(serializers.ModelSerializer):
    individual_entrepreneur = IndividualEntrepreneurSerializer()
    china_distributor = ChinaSerializer()
    order_for_project = OrderForProjectSerializer()
    status = StatusSerializer()

    class Meta:
        exclude = ('draft',)
        model = Order


class OrderCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ('draft',)
        model = Order


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Product
