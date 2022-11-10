from typing import Dict

from rest_framework import generics, views, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.request import Request
from rest_framework.response import Response

from .models import ChinaDistributor, Product, OrderForProject, Order, Status, IndividualEntrepreneur, Category, Task
from .serializer import ChinaSerializer, OrderForProjectSerializer, StatusSerializer, OrderCreateUpdateSerializer, \
    OrderListRetrieveSerializer, IndividualEntrepreneurSerializer, ProductListRetrieveSerializer, CategorySerializer, \
    TaskSerializer, ProductCreateSerializer

from .services import ChinaService

china_service = ChinaService()


class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ProductCreateSerializer
        return ProductListRetrieveSerializer


class ProductUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListRetrieveSerializer

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class FormExcelView(views.APIView):
    def put(self, request: Request):
        if not request.data['id']:
            return Response({'message': 'provide id'}, status=status.HTTP_400_BAD_REQUEST)

        id: int = int(request.data['id'])

        path = china_service.form_excel(id, request)

        return Response({'message': 'success', 'doc': path}, status=status.HTTP_200_OK)


class OrderListCreateView(generics.ListCreateAPIView):
    def get_queryset(self):
        queryset = Order.objects.all().order_by('-id')

        archive = self.request.query_params.get('archive')

        if archive is not None:
            try:
                queryset = Order.objects.filter(archive=bool(int(archive))).order_by('-id')
            except TypeError:
                pass

        return queryset

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OrderCreateUpdateSerializer
        return OrderListRetrieveSerializer


class OrderRetrieveView(generics.RetrieveDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderListRetrieveSerializer


class OrderPartialUpdateView(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderCreateUpdateSerializer

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class OrderUpdateView(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderCreateUpdateSerializer


class StatusView(generics.ListCreateAPIView):
    queryset = Status.objects.all().order_by('id')
    serializer_class = StatusSerializer


class ChinaDistributorView(generics.ListCreateAPIView):
    queryset = ChinaDistributor.objects.all()
    serializer_class = ChinaSerializer


class ChinaDistributorRetrieveDestroyUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ChinaDistributor.objects.all()
    serializer_class = ChinaSerializer


class OrderForProjectView(generics.ListCreateAPIView):
    queryset = OrderForProject.objects.all()
    serializer_class = OrderForProjectSerializer


class OrderForProjectRetrieveDestroyUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = OrderForProject.objects.all()
    serializer_class = OrderForProjectSerializer


class IndividualEntrepreneurView(generics.ListCreateAPIView):
    queryset = IndividualEntrepreneur.objects.all()
    serializer_class = IndividualEntrepreneurSerializer


class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TaskListCreateView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
