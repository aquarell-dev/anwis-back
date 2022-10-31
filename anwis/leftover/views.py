from requests import Request
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import LeftOver
from .serializers import LeftOverSerializer
from .services import LeftOverService

_leftover_service = LeftOverService()


class LeftOverView(generics.ListCreateAPIView):
    queryset = LeftOver.objects.all()
    serializer_class = LeftOverSerializer


class FetchLeftOversView(APIView):
    def put(self, request: Request):
        nms = [leftover.nm for leftover in LeftOver.objects.all()]
        try:
            _leftover_service.update_leftovers(nms)
        except Exception as e:
            return Response({"message": e}, status=400)
        return Response({"message": "success"}, status=200)