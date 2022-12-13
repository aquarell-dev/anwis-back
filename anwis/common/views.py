from rest_framework import generics

from china.serializer import IndividualEntrepreneurSerializer
from common.models import Task, Project, IndividualEntrepreneur
from common.serializers import TaskSerializer, ProjectSerializer


class TaskListCreateView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class OrderForProjectView(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class OrderForProjectRetrieveDestroyUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class IndividualEntrepreneurView(generics.ListCreateAPIView):
    queryset = IndividualEntrepreneur.objects.all()
    serializer_class = IndividualEntrepreneurSerializer