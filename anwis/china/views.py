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


class UpdateProductPhotoView(views.APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, format=None):
        data = request.data
        if isinstance(data, list):
            serializer = ProductListRetrieveSerializer(data=request.data, many=True)
        else:
            serializer = ProductListRetrieveSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FormExcelView(views.APIView):
    def put(self, request: Request):
        if not request.data['id']:
            return Response({'message': 'provide id'}, status=status.HTTP_400_BAD_REQUEST)

        id: int = int(request.data['id'])

        path = china_service.form_excel(id, request)

        return Response({'message': 'success', 'doc': path}, status=status.HTTP_200_OK)


class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OrderCreateUpdateSerializer
        return OrderListRetrieveSerializer


class OrderRetrieveView(generics.RetrieveAPIView):
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
    queryset = Status.objects.all()
    serializer_class = StatusSerializer


class ChinaDistributorView(generics.ListCreateAPIView):
    queryset = ChinaDistributor.objects.all()
    serializer_class = ChinaSerializer


class OrderForProjectView(generics.ListCreateAPIView):
    queryset = OrderForProject.objects.all()
    serializer_class = OrderForProjectSerializer


class IndividualEntrepreneurView(generics.ListCreateAPIView):
    queryset = IndividualEntrepreneur.objects.all()
    serializer_class = IndividualEntrepreneurSerializer


class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TaskListCreateView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
