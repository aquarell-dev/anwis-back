from django.urls import path

from .views import OrderListCreateView, ChinaDistributorView, OrderForProjectView, StatusView, IndividualEntrepreneurView


urlpatterns = [
    path('orders/', OrderListCreateView.as_view()),
    path('china-distributors/', ChinaDistributorView.as_view()),
    path('order-for-projects/', OrderForProjectView.as_view()),
    path('statuses/', StatusView.as_view()),
    path('individual-entrepreneurs/', IndividualEntrepreneurView.as_view()),
]
