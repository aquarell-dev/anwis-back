from rest_framework import serializers

from acceptance.models import Acceptance, StaffMember, AcceptanceCategory, Product, ProductSpecification
from china.serializer import ProductQuantityDetailedSerializer


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
    category = serializers.SlugRelatedField(slug_field='category', read_only=True)
    photo = serializers.SerializerMethodField()
    photo_id = serializers.SerializerMethodField(read_only=True)

    def get_photo(self, obj):
        request = self.context.get('request')

        if obj.photo:
            return request.build_absolute_uri(obj.photo.photo.url)

    def get_photo_id(self, obj: Product):
        if obj.photo:
            return obj.photo.id

    class Meta:
        model = Product
        fields = [
            field.name for field in Product._meta.get_fields() if field.name not in ['productspecification']
        ] + ['photo_id']


class ProductSpecificationDetailedSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        fields = '__all__'
        model = ProductSpecification


class AcceptanceListSerializer(serializers.ModelSerializer):
    products = ProductSpecificationDetailedSerializer(many=True, read_only=True)

    class Meta:
        model = Acceptance
        fields = '__all__'
