from rest_framework import serializers

from common.models import Task, Project, IndividualEntrepreneur


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Task


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Project


class IndividualEntrepreneurSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = IndividualEntrepreneur
