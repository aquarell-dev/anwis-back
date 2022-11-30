from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers

from acceptance.models import Acceptance, StaffMember, AcceptanceCategory, Product, ProductSpecification, Box, Reason, \
    AcceptanceStatus
import acceptance.service
from china.models import Order
from common.serializers import TaskSerializer


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


class ReasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reason
        fields = '__all__'


class BoxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Box
        fields = "__all__"


class ProductSpecificationSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):
    boxes = BoxSerializer(many=True)
    reasons = ReasonSerializer(many=True)

    # def update(self, instance: ProductSpecification, validated_data: dict):
    #     return update_specification(instance, validated_data)

    class Meta:
        fields = '__all__'
        model = ProductSpecification


class ProductSpecificationDetailedSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):
    product = ProductSerializer()
    boxes = BoxSerializer(many=True)
    reasons = ReasonSerializer(many=True)

    class Meta:
        fields = '__all__'
        model = ProductSpecification


class FindSpecificationByBoxSerializer(serializers.ModelSerializer):
    specification = serializers.SerializerMethodField()

    def to_representation(self, instance: Box):
        ret = super().to_representation(instance)
        return ret

    def get_specification(self, box: Box):
        return ProductSpecificationDetailedSerializer(
            acceptance.service.get_specification_by_box(box.box),
            context=self.context
        ).data

    class Meta:
        model = Box
        fields = "__all__"


class AcceptanceStatusSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = AcceptanceStatus


class AcceptanceListSerializer(serializers.ModelSerializer):
    specifications = ProductSpecificationDetailedSerializer(many=True, read_only=True)
    individual = serializers.SerializerMethodField(read_only=True)
    project = serializers.SerializerMethodField(read_only=True)
    tasks = TaskSerializer(many=True, read_only=True)
    documents = serializers.SerializerMethodField()
    status = AcceptanceStatusSerializer()

    def get_documents(self, obj):
        request = self.context.get('request')

        if obj.documents:
            return [
                {
                    "id": document.id,
                    "title": document.document.name,
                    "path": request.build_absolute_uri(document.document.url),
                } for document in obj.documents.all()
            ]

    def _get_order(self, obj: Acceptance):
        if not obj.from_order:
            return None

        order = Order.objects.filter(id=obj.from_order)

        if not order:
            return None

        return order[0]

    def get_individual(self, obj: Acceptance):
        order = self._get_order(obj)

        return order.individual_entrepreneur.individual_entrepreneur if order else None

    def get_project(self, obj: Acceptance):
        order = self._get_order(obj)

        return order.order_for_project.order_for_project if order else None

    class Meta:
        model = Acceptance
        fields = [
            field.name for field in Acceptance._meta.get_fields()
            if field.name not in ['order']
        ] + ['individual', 'project', 'documents']


class AcceptanceDetailedUpdateSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):
    specifications = ProductSpecificationSerializer(many=True)
    tasks = TaskSerializer(many=True)

    class Meta:
        model = Acceptance
        fields = '__all__'


class AcceptanceCreateSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):
    specifications = ProductSpecificationSerializer(many=True)

    class Meta:
        model = Acceptance
        fields = '__all__'
