from django.urls import path

from .views import LeftOverView, FetchLeftOversView

urlpatterns = [
    path('leftovers/', LeftOverView.as_view()),
    path('leftovers/update/', FetchLeftOversView.as_view()),
]
