from rest_framework import generics

from acceptance.models import Acceptance
from acceptance.serializers import AcceptanceListSerializer


class AcceptanceListCreateView(generics.ListCreateAPIView):
    queryset = Acceptance.objects.all()
    serializer_class = AcceptanceListSerializer


class AcceptanceRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Acceptance.objects.all()
    serializer_class = AcceptanceListSerializer
