from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers

from acceptance.models import Acceptance, StaffMember, AcceptanceCategory, Product, ProductSpecification, Box
import acceptance.service
from china.models import Order
from common.serializers import TaskSerializer


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

        if obj.photo.photo:
            return request.build_absolute_uri(obj.photo.photo.url)

    def get_photo_id(self, obj: Product):
        if obj.photo.photo:
            return obj.photo.id

    class Meta:
        model = Product
        fields = [
            field.name for field in Product._meta.get_fields() if field.name not in ['productspecification']
        ] + ['photo_id']


class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class BoxSerializer(serializers.ModelSerializer):
    def to_representation(self, instance: Box):
        ret = super().to_representation(instance)
        contents = acceptance.service.box_contents(instance.box)
        ret.update({'specification': contents})
        return ret

    class Meta:
        model = Box
        fields = "__all__"


class ProductSpecificationSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):
    boxes = BoxSerializer(many=True)
    #
    # def update(self, instance: ProductSpecification, validated_data: dict):
    #     return update_specification(instance, validated_data)

    class Meta:
        fields = '__all__'
        model = ProductSpecification


class ProductSpecificationDetailedSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):
    product = ProductSerializer()
    boxes = BoxSerializer(many=True)

    class Meta:
        fields = '__all__'
        model = ProductSpecification


class AcceptanceListSerializer(serializers.ModelSerializer):
    specifications = ProductSpecificationDetailedSerializer(many=True, read_only=True)
    individual = serializers.SerializerMethodField(read_only=True)
    project = serializers.SerializerMethodField(read_only=True)
    tasks = TaskSerializer(many=True, read_only=True)

    def _get_order(self, obj: Acceptance):
        if not obj.from_order:
            return None

        order = Order.objects.filter(id=obj.from_order)

        if not order:
            return None

        return order[0]

    def get_individual(self, obj: Acceptance):
        order = self._get_order(obj)

        return order.individual_entrepreneur.individual_entrepreneur

    def get_project(self, obj: Acceptance):
        order = self._get_order(obj)

        return order.order_for_project.order_for_project

    class Meta:
        model = Acceptance
        fields = [
            field.name for field in Acceptance._meta.get_fields()
            if field.name not in ['order']
        ] + ['individual', 'project']


class AcceptanceDetailedUpdateSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):
    specifications = ProductSpecificationSerializer(many=True)
    tasks = TaskSerializer(many=True)

    class Meta:
        model = Acceptance
        fields = '__all__'
