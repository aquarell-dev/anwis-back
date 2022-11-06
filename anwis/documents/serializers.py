from rest_framework import serializers

from .models import Document, Photo


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Document


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Photo
