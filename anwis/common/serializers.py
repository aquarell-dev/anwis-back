from rest_framework import serializers

from common.models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Task
