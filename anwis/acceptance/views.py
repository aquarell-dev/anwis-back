from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from acceptance.models import Acceptance, StaffMember, Product, AcceptanceCategory
from acceptance.serializers import AcceptanceListSerializer, AcceptanceCreateSerializer, StaffMemberSerializer, \
    ProductSerializer, CategorySerializer
from acceptance.service import create_acceptance_from_order, update_acceptance_from_order, create_label, \
    update_leftovers, update_colors, update_multiple_categories
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


class StaffMemberListCreateView(generics.ListCreateAPIView):
    queryset = StaffMember.objects.all()
    serializer_class = StaffMemberSerializer


class StaffMemberRetrieveDestroyRetrieveView(generics.RetrieveUpdateDestroyAPIView):
    queryset = StaffMember.objects.all()
    serializer_class = StaffMemberSerializer


class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductRetrieveDestroyUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class CategoryView(generics.ListCreateAPIView):
    queryset = AcceptanceCategory.objects.all()
    serializer_class = CategorySerializer


class CategoryDetailedView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AcceptanceCategory.objects.all()
    serializer_class = CategorySerializer


class GenerateLabelsView(APIView):
    def put(self, request: Request):
        mandatory_fiels = (
            'title',
            'barcode',
            'article',
            'size',
            'color',
            'quantity',
            'individual',
            'composition',
            'address',
        )

        for field in mandatory_fiels:
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
