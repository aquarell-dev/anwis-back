from rest_framework import serializers

from .models import Document, Photo


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Document


class PhotoSerializer(serializers.ModelSerializer):
    abs_url = serializers.SerializerMethodField()

    def get_abs_url(self, obj: Photo):
        req = self.context.get('request')
        return req.build_absolute_uri(obj.photo.url)

    class Meta:
        fields = ('id', 'title', 'photo', 'abs_url')
        model = Photo
