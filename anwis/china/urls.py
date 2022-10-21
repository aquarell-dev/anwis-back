from django.urls import path

from .views import OrderListCreateView, ChinaDistributorView, OrderForProjectView, StatusView, IndividualEntrepreneurView


urlpatterns = [
    path('orders/', OrderListCreateView.as_view()),
    path('china-distributor/', ChinaDistributorView.as_view()),
    path('order-for-project/', OrderForProjectView.as_view()),
    path('status/', StatusView.as_view()),
    path('individual-entrepreneur/', IndividualEntrepreneurView.as_view()),
]
