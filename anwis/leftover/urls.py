from django.urls import path

from .views import LeftOverView, FetchLeftOversView, ResetCacheView

urlpatterns = [
    path('leftovers/', LeftOverView.as_view()),
    path('leftovers/update/', FetchLeftOversView.as_view()),
    path('leftovers/reset-cache/', ResetCacheView.as_view()),
]
