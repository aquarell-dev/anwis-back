from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers

from .models import ChinaDistributor, Product, OrderForProject, Order, Status, IndividualEntrepreneur, ProductQuantity,\
    Category, Task


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


class ProductListRetrieveSerializer(serializers.ModelSerializer):
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
        fields = [field.name for field in Product._meta.get_fields() if field.name not in ['productquantity']] + ['photo_id']
        model = Product


class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Product


class ProductQuantitySerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = ProductQuantity


class ProductQuantityDetailedSerializer(ProductQuantitySerializer):
    product = ProductListRetrieveSerializer()

    class Meta(ProductQuantitySerializer.Meta):
        pass


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Category


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Task


class OrderListRetrieveSerializer(serializers.ModelSerializer):
    individual_entrepreneur = IndividualEntrepreneurSerializer()
    china_distributor = ChinaSerializer()
    order_for_project = OrderForProjectSerializer()
    status = StatusSerializer()
    products = ProductQuantityDetailedSerializer(many=True)
    tasks = TaskSerializer(many=True)
    documents = serializers.SerializerMethodField()

    def get_documents(self, obj: Order):
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
        fields = [field.name for field in Order._meta.get_fields()]
        model = Order


class OrderCreateSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):
    products = ProductQuantitySerializer(many=True)

    class Meta:
        fields = '__all__'
        model = Order


class OrderUpdateSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):
    products = ProductQuantitySerializer(many=True)
    tasks = TaskSerializer(many=True)

    class Meta:
        fields = '__all__'
        model = Order


class OrderRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Order
