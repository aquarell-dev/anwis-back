from rest_framework import generics

from acceptance.models import Acceptance
from acceptance.serializers import AcceptanceListSerializer, AcceptanceCreateSerializer


class AcceptanceListCreateView(generics.ListCreateAPIView):
    queryset = Acceptance.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AcceptanceCreateSerializer
        return AcceptanceListSerializer


class AcceptanceRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Acceptance.objects.all()
    serializer_class = AcceptanceListSerializer
