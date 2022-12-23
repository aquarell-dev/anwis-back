from datetime import datetime, timedelta
from typing import List

from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from acceptance.models import (
    Acceptance,
    StaffMember,
    Product,
    AcceptanceCategory,
    ProductSpecification,
    Box,
    Reason,
    AcceptanceStatus, WorkSession, Payment, TimeSession
)
from acceptance.serializers import (
    AcceptanceRetrieveSerializer,
    AcceptanceCreateSerializer,
    StaffMemberSerializer,
    ProductSerializer,
    CategorySerializer,
    ProductCreateSerializer,
    AcceptanceDetailedSerializer,
    ProductSpecificationSerializer,
    BoxSerializer,
    ReasonSerializer,
    AcceptanceStatusSerializer,
    StaffMemberCreateSerializer,
    AcceptanceListSerializer, BoxDetailedSerializer, StaffMemberDetailedSerializer, StaffMemberBoxDetailedSerializer,
    WorkSessionSerializer, WorkSessionWithStaffSerializer, PaymentSerializer, TimeSessionSerializer
)
from acceptance.service import (
    create_acceptance_from_order,
    update_acceptance_from_order,
    update_leftovers,
    update_colors,
    update_multiple_categories,
    create_multiple_products,
    update_photos_from_wb,
    update_specification,
    get_specification_by_box,
    get_specification_by_barcode, update_multiple_specifications, create_labels, add_null_box
)
from china.models import Order
from common.services import check_required_keys


# ***********************************************************************
# Acceptance
# ***********************************************************************


class AcceptanceListCreateView(generics.ListCreateAPIView):
    queryset = Acceptance.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AcceptanceCreateSerializer
        return AcceptanceListSerializer

    def get_serializer(self, *args, **kwargs):
        return super().get_serializer(*args, **kwargs)


class AcceptanceRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Acceptance.objects.all()
    serializer_class = AcceptanceRetrieveSerializer


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
    serializer_class = AcceptanceDetailedSerializer

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


# ***********************************************************************
# Status
# ***********************************************************************


class StatusListView(generics.ListAPIView):
    queryset = AcceptanceStatus.objects.all()
    serializer_class = AcceptanceStatusSerializer


# ***********************************************************************
# Specifications
# ***********************************************************************


class CreateMultipleSpecificationsView(APIView):
    def post(self, request):
        acceptance: Acceptance = get_object_or_404(Acceptance.objects.all(), id=request.data.pop('id', None))

        products = request.data.pop('products', None)

        if not products:
            return Response({'status': 'error', 'message': 'provide product ids'}, status=400)

        for product in products:
            id = product.pop('product', None)

            if not id:
                continue

            quantity = product.pop('quantity', 0)

            specification = acceptance.specifications.create(
                cost=0,
                quantity=int(quantity),
                product_id=int(id)
            )

            add_null_box(specification)

        return Response({'status': 'ok'}, status=200)


class ProductSpecificationPartialUpdateView(generics.UpdateAPIView):
    queryset = ProductSpecification.objects.all()
    serializer_class = ProductSpecificationSerializer

    def put(self, request, *args, **kwargs):
        instance = update_specification(self.get_object(), request.data)
        instance.save()
        serializer = ProductSpecificationSerializer(instance)
        return Response(serializer.data)


class ProductSpecificationPartialMultipleUpdateView(APIView):
    def put(self, request, *args, **kwargs):
        response = update_multiple_specifications(request)

        return Response(response, status=200)


class AddBlankBoxToSpecification(generics.UpdateAPIView):
    queryset = ProductSpecification.objects.all()
    serializer_class = ProductSpecificationSerializer

    def put(self, request, *args, **kwargs):
        instance: ProductSpecification = self.get_object()
        instance.boxes.create(
            box='',
            quantity=0,
            specification=instance
        )
        serializer = ProductSpecificationSerializer(instance)
        return Response(serializer.data)


class AddReasonToSpecification(generics.UpdateAPIView):
    queryset = ProductSpecification.objects.all()
    serializer_class = ProductSpecificationSerializer

    def put(self, request, *args, **kwargs):
        instance: ProductSpecification = self.get_object()
        instance.reasons.create(
            reason='',
            quantity=0
        )
        serializer = ProductSpecificationSerializer(instance)
        return Response(serializer.data)


# ***********************************************************************
# Staff
# ***********************************************************************


class StaffMemberListCreateView(generics.ListCreateAPIView):
    queryset = StaffMember.objects.all().order_by('unique_number')

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return StaffMemberCreateSerializer
        return StaffMemberDetailedSerializer


class StaffMemberRetrieveDestroyRetrieveView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'unique_number'

    queryset = StaffMember.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return StaffMemberSerializer
        return StaffMemberDetailedSerializer

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class StaffMemberUpdateDetailedView(StaffMemberRetrieveDestroyRetrieveView):
    def get_serializer_class(self):
        return StaffMemberBoxDetailedSerializer


# ***********************************************************************
# Product
# ***********************************************************************


class ProductListCreateView(generics.ListCreateAPIView):
    def get_queryset(self):
        queryset = Product.objects.all()

        barcode = self.request.query_params.get('barcode')

        if barcode is not None:
            queryset = queryset.filter(barcode=barcode)

        return queryset

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


class ProductRetrieveByBarcodeView(generics.RetrieveAPIView):
    lookup_field = 'barcode'

    queryset = Product.objects.all()
    serializer_class = ProductSerializer


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


# ***********************************************************************
# Category
# ***********************************************************************


class CategoryView(generics.ListCreateAPIView):
    queryset = AcceptanceCategory.objects.all()
    serializer_class = CategorySerializer


class CategoryDetailedView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AcceptanceCategory.objects.all()
    serializer_class = CategorySerializer


class UpdateMultipleCategoriesView(APIView):
    def put(self, request):
        status = update_multiple_categories(request.data)

        if status == 0:
            return Response({'status': 'error'}, status=400)

        return Response({'status': 'ok'}, status=200)


# ***********************************************************************
# Additional
# ***********************************************************************


class GenerateLabelsView(APIView):
    def post(self, request: Request):
        mandatory_fields = [
            # 'title',
            # 'barcode',
            # 'article',
            # 'size',
            # 'color',
            # 'quantity',
            # 'individual',
            # 'composition',
            # 'address',
            # 'category',
            'products'
        ]

        for field in mandatory_fields:
            try:
                request.data[field]
            except KeyError:
                return Response({'status': 'error', 'message': f'provide {field} field'}, status=400)

        products: List[Product] = create_labels(request.data)

        return Response(
            ProductSerializer(
                products,
                many=True,
                context={'request': request, 'format': self.format_kwarg, 'view': self}
            ).data,
            status=200
        )


class UpdateProductLeftoversView(APIView):
    def put(self, *args, **kwargs):
        update_leftovers()
        return Response({'status': 'ok'}, status=200)


class UpdateProductColorsView(APIView):
    def put(self, *args, **kwargs):
        update_colors()
        return Response({'status': 'ok'}, status=200)


class FindSpecificationByBox(APIView):
    def post(self, request: Request):
        missing = check_required_keys(request.data, 'box_number')

        if missing:
            return Response({'status': 'error', 'found missing properties': ', '.join(missing)}, status=400)

        context = {'request': request, 'format': self.format_kwarg, 'view': self}

        return get_specification_by_box(context, **request.data)


class FindSpecificationByBarcode(generics.RetrieveAPIView):
    def post(self, request: Request):
        missing = check_required_keys(request.data, 'barcode')

        if missing:
            return Response({'status': 'error', 'found missing properties': ', '.join(missing)}, status=400)

        context = {'request': request, 'format': self.format_kwarg, 'view': self}
        return get_specification_by_barcode(context, **request.data)


class ParsePhotosView(APIView):
    def put(self, request):
        articles = request.data.pop('articles', None)

        if not articles:
            return Response({'status': 'error'}, status=400)

        update_photos_from_wb(articles)

        return Response({'status': 'ok'}, status=200)


# ***********************************************************************
# Box
# ***********************************************************************


class RetrieveDeleteUpdateBoxView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Box.objects.all()
    serializer_class = BoxSerializer

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class RetrieveBoxByBoxNumber(generics.RetrieveAPIView):
    lookup_field = 'box'
    queryset = Box.objects.filter(
        productspecification__acceptance__status__in=['Новая Приемка', 'Упаковано', 'Упаковывается'],
        specification__isnull=False,
        quantity__gt=0
    )
    serializer_class = BoxDetailedSerializer


# ***********************************************************************
# Reason
# ***********************************************************************


class RetrieveDeleteReasonView(generics.RetrieveDestroyAPIView):
    queryset = Reason.objects.all()
    serializer_class = ReasonSerializer


# ***********************************************************************
# Session
# ***********************************************************************


class WorkSessionListByAcceptanceView(generics.ListAPIView):
    serializer_class = WorkSessionWithStaffSerializer

    def get_queryset(self):
        queryset = WorkSession.objects.filter(legit=True)

        acceptance = self.request.query_params.get('acceptance')
        box = self.request.query_params.get('box')
        today = self.request.query_params.get('today')

        if acceptance is not None:
            try:
                int(acceptance)
            except ValueError:
                return Response({'error': 'provide acceptance id'}, status=400)

            queryset = queryset.filter(box__specification__acceptance=int(acceptance), end__isnull=False)

        if box is not None:
            queryset = queryset.filter(box__box=str(box))

        if today is not None and today == '1':
            queryset = queryset.filter(
                start__range=[datetime.today().strftime('%Y-%m-%d'),
                              (datetime.today() + timedelta(hours=24)).strftime('%Y-%m-%d')])

        return queryset


class WorkSessionRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = WorkSession.objects.all()
    serializer_class = WorkSessionSerializer


class TimeSessionRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TimeSession.objects.all()
    serializer_class = TimeSessionSerializer


# ***********************************************************************
# Payment
# ***********************************************************************


class RetrieveUpdatePaymentView(generics.RetrieveUpdateAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
