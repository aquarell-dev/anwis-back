import random

from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers

from acceptance.models import Acceptance, StaffMember, AcceptanceCategory, Product, ProductSpecification, Box, Reason, \
    AcceptanceStatus, Session
from china.models import Order
from common.serializers import TaskSerializer


# ***********************************************************************
# Session
# ***********************************************************************


class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Session


# ***********************************************************************
# Staff
# ***********************************************************************


class StaffMemberSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):
    session = SessionSerializer()

    class Meta:
        fields = '__all__'
        model = StaffMember


class StaffMemberCreateSerializer(StaffMemberSerializer):
    def create(self, validated_data):
        unique_number = validated_data.pop('unique_number', None)

        return StaffMember.objects.create(
            **validated_data,
            unique_number=unique_number if unique_number else str(random.randint(1, 100))
        )

    class Meta(StaffMemberSerializer.Meta):
        pass


# ***********************************************************************
# Category
# ***********************************************************************


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = AcceptanceCategory


# ***********************************************************************
# Product
# ***********************************************************************


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
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


class ProductBarcodeSerializer(ProductSerializer):
    def to_representation(self, instance):
        if len(instance) == 0:
            print('len 0')
        else:
            print(len(instance))
        ret = super().to_representation(instance)
        return ret

    class Meta(ProductSerializer.Meta):
        pass


class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


# ***********************************************************************
# Reason
# ***********************************************************************


class ReasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reason
        fields = '__all__'


# ***********************************************************************
# Box
# ***********************************************************************


class BoxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Box
        fields = "__all__"


# ***********************************************************************
# Specification
# ***********************************************************************


class ProductSpecificationSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):
    boxes = BoxSerializer(many=True)
    reasons = ReasonSerializer(many=True)

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


# ***********************************************************************
# Detailed
# ***********************************************************************


class BoxDetailedSerializer(serializers.ModelSerializer):
    specification = ProductSpecificationDetailedSerializer(read_only=True)

    class Meta:
        model = Box
        fields = "__all__"


class StaffMemberDetailedSerializer(serializers.ModelSerializer):
    box = BoxDetailedSerializer(read_only=True)

    class Meta:
        model = StaffMember
        fields = "__all__"


# ***********************************************************************
# Status
# ***********************************************************************


class AcceptanceStatusSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = AcceptanceStatus


# ***********************************************************************
# Acceptance
# ***********************************************************************


class AcceptanceListSerializer(serializers.ModelSerializer):
    specifications = ProductSpecificationDetailedSerializer(many=True, read_only=True)

    class Meta:
        fields = ['id', 'title', 'specifications', 'created_at', 'from_order']
        model = Acceptance


class AcceptanceRetrieveSerializer(serializers.ModelSerializer):
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
