from django.urls import path

from acceptance.views import AcceptanceListCreateView, AcceptanceRetrieveUpdateDestroyView

urlpatterns = [
    path('acceptances/', AcceptanceListCreateView.as_view()),
    path('acceptances/<int:pk>/', AcceptanceRetrieveUpdateDestroyView.as_view()),
]
