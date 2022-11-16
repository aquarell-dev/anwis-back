from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from acceptance.models import Acceptance, StaffMember, Product, AcceptanceCategory
from acceptance.serializers import AcceptanceListSerializer, AcceptanceCreateSerializer, StaffMemberSerializer, \
    ProductSerializer, CategorySerializer
from acceptance.service import create_acceptance_from_order, update_acceptance_from_order
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

        create_acceptance_from_order(order)

        return Response({'status': 'ok'}, status=201)


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


class CategoryView(generics.ListCreateAPIView):
    queryset = AcceptanceCategory
    serializer_class = CategorySerializer
