from rest_framework import generics
from rest_framework.response import Response

from .models import ChinaDistributor, Product, OrderForProject, Order, Status, IndividualEntrepreneur
from .serializer import ChinaSerializer, OrderForProjectSerializer, StatusSerializer, OrderCreateUpdateSerializer, \
    OrderListRetrieveSerializer, IndividualEntrepreneurSerializer


class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.filter(draft=False)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OrderCreateUpdateSerializer
        return OrderListRetrieveSerializer


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
