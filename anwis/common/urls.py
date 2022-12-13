from django.urls import path

from common.views import TaskListCreateView, IndividualEntrepreneurView, OrderForProjectView, \
    OrderForProjectRetrieveDestroyUpdateView

urlpatterns = [
    path('tasks/', TaskListCreateView.as_view()),
    path('individual-entrepreneurs/', IndividualEntrepreneurView.as_view()),

    path('projects/', OrderForProjectView.as_view()),
    path('projects/<int:pk>/', OrderForProjectRetrieveDestroyUpdateView.as_view()),
]
