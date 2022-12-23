import random

from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers

from acceptance.models import Acceptance, StaffMember, AcceptanceCategory, Product, ProductSpecification, Box, Reason, \
    AcceptanceStatus, WorkSession, TimeSession, Payment
from china.models import Project
from common.serializers import TaskSerializer, ProjectSerializer, IndividualEntrepreneurSerializer


# ***********************************************************************
# Session
# ***********************************************************************


class WorkSessionSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = WorkSession


class TimeSessionSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = TimeSession


# ***********************************************************************
# Staff
# ***********************************************************************


class MinimalisticStaffSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'username', 'unique_number')
        model = StaffMember


class StaffMemberSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):
    work_session = WorkSessionSerializer(allow_null=True)
    time_session = TimeSessionSerializer(allow_null=True)
    work_sessions = WorkSessionSerializer(many=True)

    class Meta:
        fields = '__all__'
        model = StaffMember


class StaffMemberCreateSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        unique_number = validated_data.pop('unique_number', None)

        try:
            possible_unique_number = min([int(staff.unique_number) for staff in StaffMember.objects.all()])
        except ValueError:
            possible_unique_number = 1

        return StaffMember.objects.create(
            **validated_data,
            unique_number=unique_number if unique_number else possible_unique_number
        )

    class Meta(StaffMemberSerializer.Meta):
        fields = '__all__'
        model = StaffMember


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


class MinimalisticBoxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Box
        fields = ('id', 'box', 'finished', 'quantity')


class BoxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Box
        fields = "__all__"


# ***********************************************************************
# Payment
# ***********************************************************************


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
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


class WorkSessionBoxDetailedSerializer(serializers.ModelSerializer):
    box = BoxDetailedSerializer()

    class Meta:
        model = WorkSession
        fields = '__all__'


class WorkSessionWithStaffSerializer(WorkSessionBoxDetailedSerializer):
    box = MinimalisticBoxSerializer()

    def to_representation(self, instance: WorkSession):
        ret = super(WorkSessionWithStaffSerializer, self).to_representation(instance)
        s = MinimalisticStaffSerializer(StaffMember.objects.filter(work_sessions__in=[instance]).first())
        ret.update({'staff': s.data})
        return ret

    class Meta(WorkSessionBoxDetailedSerializer.Meta):
        pass


class StaffMemberDetailedSerializer(serializers.ModelSerializer):
    box = BoxDetailedSerializer(read_only=True)
    time_session = TimeSessionSerializer()
    work_session = WorkSessionBoxDetailedSerializer()
    time_sessions = TimeSessionSerializer(many=True, read_only=True)
    work_sessions = WorkSessionBoxDetailedSerializer(many=True, read_only=True)

    class Meta:
        model = StaffMember
        fields = "__all__"


class StaffMemberBoxDetailedSerializer(WritableNestedModelSerializer, StaffMemberDetailedSerializer):
    box = BoxDetailedSerializer(read_only=False)


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
    status = AcceptanceStatusSerializer()

    class Meta:
        fields = ['id', 'title', 'specifications', 'created_at', 'from_order', 'status']
        model = Acceptance


class AcceptanceRetrieveSerializer(serializers.ModelSerializer):
    specifications = ProductSpecificationDetailedSerializer(many=True, read_only=True)
    individual = IndividualEntrepreneurSerializer()
    project = ProjectSerializer()
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

    class Meta:
        model = Acceptance
        fields = [
                     field.name for field in Acceptance._meta.get_fields()
                     if field.name not in ['order']
                 ] + ['documents']


class AcceptanceDetailedSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):
    specifications = ProductSpecificationSerializer(many=True)
    tasks = TaskSerializer(many=True)

    class Meta:
        fields = '__all__'
        model = Acceptance


class AcceptanceCreateSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):
    specifications = ProductSpecificationSerializer(many=True)

    class Meta:
        model = Acceptance
        fields = '__all__'
