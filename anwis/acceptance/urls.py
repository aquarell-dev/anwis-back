from django.urls import path

from acceptance.views import AcceptanceListCreateView

urlpatterns = [
    path('acceptances/', AcceptanceListCreateView.as_view()),
]
