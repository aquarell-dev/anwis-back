from rest_framework import serializers

from .models import Document, Photo


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Document


class PhotoSerializer(serializers.ModelSerializer):
    # abs_url = serializers.SerializerMethodField()
    #
    # def get_abs_url(self, obj: Photo):
    #     req = self.context.get('request')
    #     return req.build_absolute_uri(obj.photo.url)

    class Meta:
        fields = ('id', 'title', 'photo')
        model = Photo


class DocumentMixin:
    documents = serializers.SerializerMethodField()
    request = None

    def get_documents(self, obj):
        # request = self.context.get('request')

        if obj.documents:
            return [
                {
                    "id": document.id,
                    "title": document.document.name,
                    "path": self.request.build_absolute_uri(document.document.url),
                } for document in obj.documents.all()
            ]
