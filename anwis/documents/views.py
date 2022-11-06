from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import DocumentSerializer, PhotoSerializer


class DocumentView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, format=None):
        serializer = DocumentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PhotoView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, format=None):
        serializer = PhotoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
