from rest_framework import generics

from .models import ChinaDistributor, Product, OrderForProject, Order, Status, IndividualEntrepreneur, Category, Task
from .serializer import ChinaSerializer, OrderForProjectSerializer, StatusSerializer, OrderCreateUpdateSerializer, \
    OrderListRetrieveSerializer, IndividualEntrepreneurSerializer, ProductSerializer, CategorySerializer, TaskSerializer


class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


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
