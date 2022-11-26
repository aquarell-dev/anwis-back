from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from rest_framework.views import APIView

from acceptance.models import Acceptance, StaffMember, Product, AcceptanceCategory, ProductSpecification, Box
from acceptance.serializers import AcceptanceListSerializer, AcceptanceCreateSerializer, StaffMemberSerializer, \
    ProductSerializer, CategorySerializer, ProductCreateSerializer, AcceptanceDetailedUpdateSerializer, \
    ProductSpecificationSerializer, BoxSerializer
from acceptance.service import create_acceptance_from_order, update_acceptance_from_order, create_label, \
    update_leftovers, update_colors, update_multiple_categories, create_multiple_products, update_photos_from_wb, \
    update_specification, box_contents
from china.models import Order


class AcceptanceListCreateView(generics.ListCreateAPIView):
    queryset = Acceptance.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AcceptanceCreateSerializer
        return AcceptanceListSerializer


class AcceptanceRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Acceptance.objects.all()
    serializer_class = AcceptanceListSerializer


class AcceptanceCreateFromOrder(APIView):
    def post(self, request: Request):
        order_id = request.data.get('order_id', None)

        if not order_id:
            return Response({'status': 'error'}, status=400)

        order = get_object_or_404(Order, pk=order_id)

        acceptance = create_acceptance_from_order(order)

        return Response({'status': 'ok', 'acceptance_id': acceptance.id}, status=201)


class AcceptanceUpdateFromOrder(APIView):
    def put(self, request: Request):
        order_id = request.data.get('order_id', None)

        if not order_id:
            return Response({'status': 'error'}, status=400)

        acceptance_id = request.data.get('acceptance_id', None)

        if not acceptance_id:
            return Response({'status': 'error'}, status=400)

        order = get_object_or_404(Order, pk=order_id)

        acceptance = get_object_or_404(Acceptance, pk=acceptance_id)

        update_acceptance_from_order(acceptance, order)

        return Response({'status': 'ok'}, status=201)


class AcceptanceDetailedUpdate(generics.UpdateAPIView):
    queryset = Acceptance.objects.all()
    serializer_class = AcceptanceDetailedUpdateSerializer

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class ProductSpecificationPartialUpdateView(generics.UpdateAPIView):
    queryset = ProductSpecification.objects.all()
    serializer_class = ProductSpecificationSerializer

    def put(self, request, *args, **kwargs):
        instance = update_specification(self.get_object(), request.data)
        serializer = ProductSpecificationSerializer(instance)
        return Response(serializer.data)

    # def put(self, request, *args, **kwargs):
    #     return self.partial_update(request, *args, **kwargs)


class ProductSpecificationPartialMultipleUpdateView(APIView):
    def put(self, request):
        specifications = request.data.pop('specifications', None)

        if not specifications:
            return Response({'error': 'provise specs'}, status=400)

        response = []

        for specification in specifications:
            id = specification.pop('id', None)

            if not id:
                continue

            try:
                specification_instance = ProductSpecification.objects.get(id=int(id))
            except ProductSpecification.DoesNotExist:
                continue

            update_specification(specification_instance, specification)

            response.append({'id': specification_instance.id, 'status': 'updated'})

        return Response(response, status=200)


class StaffMemberListCreateView(generics.ListCreateAPIView):
    queryset = StaffMember.objects.all()
    serializer_class = StaffMemberSerializer


class StaffMemberRetrieveDestroyRetrieveView(generics.RetrieveUpdateDestroyAPIView):
    queryset = StaffMember.objects.all()
    serializer_class = StaffMemberSerializer


class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ProductCreateSerializer
        return ProductSerializer


class ProductRetrieveDestroyUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ProductSerializer
        return ProductCreateSerializer

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class DeleteMultipleProductsView(APIView):
    def put(self, request):
        delete_products_ids = request.data.pop('products', None)

        if not delete_products_ids:
            return Response({'status': 'error', 'message': 'provide product ids'}, status=400)

        Product.objects.filter(id__in=delete_products_ids).delete()

        return Response({'status': 'ok'}, status=204)


class DeleteMultipleSpecificationsView(APIView):
    def put(self, request):
        delete_specification_ids = request.data.pop('specifications', None)

        if not delete_specification_ids:
            return Response({'status': 'error', 'message': 'provide specification ids'}, status=400)

        ProductSpecification.objects.filter(id__in=delete_specification_ids).delete()

        return Response({'status': 'ok'}, status=204)


class CreateMultipleProducts(APIView):
    def post(self, request):
        products = request.data.pop('products', None)

        if not products:
            return Response({'status': 'error', 'message': 'provide products'}, status=200)

        create_multiple_products(products)

        return Response({'status': 'ok'}, status=200)


class CategoryView(generics.ListCreateAPIView):
    queryset = AcceptanceCategory.objects.all()
    serializer_class = CategorySerializer


class CategoryDetailedView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AcceptanceCategory.objects.all()
    serializer_class = CategorySerializer


class GenerateLabelsView(APIView):
    def put(self, request: Request):
        mandatory_fields = (
            'title',
            'barcode',
            'article',
            'size',
            'color',
            'quantity',
            'individual',
            'composition',
            'address',
            'category'
        )

        for field in mandatory_fields:
            try:
                request.data[field]
            except KeyError:
                return Response({'status': 'error', 'message': f'provide {field} field'}, status=400)

        url = create_label(request.data)

        return Response({'status': 'ok', 'url': request.build_absolute_uri(url)}, status=200)


class UpdateProductLeftoversView(APIView):
    def put(self, *args, **kwargs):
        update_leftovers()
        return Response({'status': 'ok'}, status=200)


class UpdateProductColorsView(APIView):
    def put(self, *args, **kwargs):
        update_colors()
        return Response({'status': 'ok'}, status=200)


class UpdateMultipleCategoriesView(APIView):
    def put(self, request):
        status = update_multiple_categories(request.data)

        if status == 0:
            return Response({'status': 'error'}, status=400)

        return Response({'status': 'ok'}, status=200)


class ParsePhotosView(APIView):
    def put(self, request):
        articles = request.data.pop('articles', None)

        if not articles:
            return Response({'status': 'error'}, status=400)

        update_photos_from_wb(articles)

        return Response({'status': 'ok'}, status=200)


class AddBoxToSpecification(generics.UpdateAPIView):
    queryset = ProductSpecification.objects.all()
    serializer_class = ProductSpecificationSerializer

    def put(self, request, *args, **kwargs):
        instance: ProductSpecification = self.get_object()
        instance.boxes.create(
            box='',
            quantity=0
        )
        serializer = ProductSpecificationSerializer(instance)
        return Response(serializer.data)


class RetrieveDeleteBoxView(generics.RetrieveDestroyAPIView):
    queryset = Box.objects.all()
    serializer_class = BoxSerializer


class GetProductByBoxNumber(generics.RetrieveAPIView):
    lookup_field = 'box'

    queryset = Box.objects.all()
    serializer_class = BoxSerializer
